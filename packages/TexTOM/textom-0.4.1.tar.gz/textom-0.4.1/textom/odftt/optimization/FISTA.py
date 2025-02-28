from tqdm import tqdm
import numpy as np


class FISTA():
    """ Basic implementation of the FISTA optimizer for L1 regularized least-sqares problems.

    Parameters:
    -----------
        model
            an object from `odftt.tomography_models`. Contains some implementation of the
            system matrix in the two methods `model.forward` and `model.adjoint`.
        data_array
            a 5-d numpy array containing the dataset.
            Dimension 0 is the projection index. Dimensions 1 and 2 are the raster scan.
            If using a 2D slice, leave dimension 2 with 1-length. Dimenstion 3 is the
            detector azimuth angle. Dimension 4 is the Bragg-peak number.
        x0 (optional)
            Initial guess for the solution array. Shape must be compatible with `model`.
        weights (optional)
            Weight array for weighed optimization. Same shape as data_array or castable.
        regularization_weigth (optional)
            Regularization parameter. Default `0` is equivalent to the unregularized problem.
        step_size_parameter (optional)
            Step-size parameter. Should be no larger that one over the matrix norm of the
            system matrix. (largest singular value). Per default this value will be estimated
            by the power method.
        maxiter (optional)
            Number of iterations. Default is `100`
        nonneg (optional)
            Bool flag to determine whether to enforce non-negativity of the coefficients
            or not. Default `True` enforces non-negativity.
        volume_mask (optional)
            Numpy array of booleans same shape as reconstructed tomogram. Used to reconstruct
            only inside a sample support.
    """

    def __init__(self, model, data_array, x0=None, weights=None, regularization_weigth=0.0,
                 step_size_parameter=None, maxiter=100, nonneg=True, volume_mask=None):

        self.model = model
        self.data = data_array
        self.nonneg = nonneg
        self.volume_mask = volume_mask

        if x0 is None:
            self.x0 = np.zeros((*model.volume_shape, model.n_modes))
        else:
            self.x0 = x0

        if weights is None:
            self.weights = np.ones(data_array.shape)
        else:
            self.weights = weights

        # Estimate a safe step-size
        if step_size_parameter is None:
            print('Estimating largest safe step size')
            x = np.random.normal(loc=0.0, scale=1.0, size=(*model.volume_shape, model.n_modes))
            # First iteration
            xnorm = np.sqrt(np.sum(x**2))
            x = x / xnorm
            x = model.adjoint(model.forward(x))
            xnorm = np.sqrt(np.sum(x**2))
            # Setting up nice progress bar
            iterator = tqdm(range(10))
            iterator.set_description(f"Matrix norm estimate = {xnorm:.2E}")
            for ii in iterator:
                x = x / xnorm
                x = model.adjoint(model.forward(x))
                xnorm_old = xnorm
                xnorm = np.sqrt(np.sum(x**2))
                iterator.set_description(f"Matrix norm estimate = {xnorm:.2E}")
                # Stopping rule for less than 5 percent change
                if xnorm / xnorm_old < 1.05:
                    break

            self.step_size_parameter = 1/xnorm
        else:
            self.step_size_parameter = step_size_parameter

        self.regularization_weigth = regularization_weigth
        self.maxiter = maxiter

    def step(self, x, y, t):
        """ Single step of the optimization routine.
        """
        x_old = np.copy(x)
        res = self.data - self.model.forward(y)
        bp_res = self.model.adjoint(res * self.weights)

        if self.volume_mask is not None:
            bp_res[~self.volume_mask] = 0.0

        x = y + self.step_size_parameter * bp_res

        # lasso proximal
        if self.nonneg:
            x = x - self.regularization_weigth * self.step_size_parameter
            np.clip(x, 0, np.inf, out=x)
        else:
            mask = self.regularization_weigth * self.step_size_parameter >= np.abs(x)
            x = x - self.regularization_weigth * self.step_size_parameter
            x[mask] = 0

        t_old = t
        t = (1+np.sqrt(1+4*t**2))/2
        y = x + (t_old - 1) / t * (x - x_old)
        cost = np.sum(res**2*self.weights) + self.regularization_weigth * np.sum(np.abs(x))
        return x, y, t, cost

    def optimize(self):
        """ Optimization routine of the FISTA algorithm.
        """

        # initializing arrays
        x = np.copy(self.x0)
        y = np.copy(x)
        t = 1

        # initial value of cost function
        res = self.data - self.model.forward(y)
        cost = np.sum(res**2*self.weights) + self.regularization_weigth * np.sum(np.abs(x))

        # Set up nice progress bar
        iterator = tqdm(range(self.maxiter))
        iterator.set_description(f"Loss = {cost:.2E}")
        convergence_curve = [cost]
        for ii in iterator:
            x, y, t, cost = self.step(x, y, t)
            iterator.set_description(f"Loss = {cost:.2E}")
            convergence_curve.append(cost)

        return x, np.array(convergence_curve)
