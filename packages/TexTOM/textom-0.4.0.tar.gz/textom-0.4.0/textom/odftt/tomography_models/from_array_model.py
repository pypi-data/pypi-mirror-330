from mumott.methods.projectors import SAXSProjector as Projector
import numpy as np


class FromArrayModel():
    """
    Object responsible for calculating the forward model by composing the pole-figure arrays calculated by
    an  `odftt.texture.odfs` object and computing x-ray transforms.

    On initialization, it computes the pole-figure matrices which is typically slow for the grid type
    basis sets.

    Parameters
    ----------
        basisfunction_values
            Arrays of pre-computed basis-function values. One array for each sample rotations.
            shape of arrays is the number of basis function modes times the number of detector channels
            i.e. "# of azimuthal channels" times "# of hkl rings"

        geom
            `mumott`-style geometry object. only used to initialize the projector object.

    """

    def __init__(self, basisfunction_values, geom):

        self.n_projections = len(geom)

        # Figure out how the geometry maps into the basis-function arrays:
        N_basisfunctions = basisfunction_values[0].shape[0]
        N_detector_channels = basisfunction_values[0].shape[1]
        N_azim_channels = len(geom.detector_angles)
        N_hkl_rings = N_detector_channels//N_azim_channels

        self.channels_shape = (N_azim_channels, N_hkl_rings)
        self.volume_shape = geom.volume_shape
        self.image_shape = geom.projection_shape
        self.projector = Projector(geom)
        self.n_modes = N_basisfunctions
        self.basisfunctions = basisfunction_values

    def forward(self, coeffs):
        """ Evaluation of the forward model:

        Parameters:
        -----------
        coeffs (np.array):
            numpy array containging the coefficient of the tomograms.
            Shape is (x, y, z, odf basis function number)

        Returns:
        --------
            Numpy array containing the forward model evaluated on the coefficients.
            Shape is (sample rotation, raster index 1, raster index 2,
            detector azimuth angle, bragg peak index)
        """

        proj_coeffs = self.projector.forward(coeffs.astype(self.projector.dtype))\
            .reshape((self.n_projections, np.product(self.image_shape), self.n_modes))
        model_I = np.zeros((self.n_projections, *self.image_shape, *self.channels_shape))

        for ii in range(self.n_projections):
            model_I[ii, ...] = (proj_coeffs[ii, ...] @ self.basisfunctions[ii])\
                .reshape((*self.image_shape, *self.channels_shape))
        return model_I

    def adjoint(self, residual):
        """ Evaluation of the adjoint of the forward model:

        Parameters:
        -----------
        residual (np.array):
            Numpy array containing typically the residual of the fit but can by any data-shaped array.
            Shape is (sample rotation, raster index 1, raster index 2, detector azimuth angle,
            bragg peak index)

        Returns:
        --------
            Numpy array containing the computed backprojection. Shape is (x, y, z, odf basis function number)
        """

        modes = np.zeros((self.n_projections, np.product(self.image_shape), self.n_modes))
        matrix_shape = (np.product(self.image_shape), np.product(self.channels_shape))

        for ii in range(self.n_projections):
            modes[ii, ...] = (residual[ii, ...].reshape(matrix_shape) @ self.basisfunctions[ii].T)

        modes = modes.reshape((self.n_projections, *self.image_shape, self.n_modes))
        coeffs = self.projector.adjoint(modes.astype(self.projector.dtype))
        return coeffs
