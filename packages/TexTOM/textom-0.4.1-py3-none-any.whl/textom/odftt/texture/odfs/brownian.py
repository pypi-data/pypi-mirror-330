import numpy as np
from multiprocessing import Pool
import time
from datetime import timedelta
from scipy.sparse import csr_array


class Brownian:
    """ Representation of a grid-based model of an Orientation Distribution Function (ODF)
    with a Gassian kernel function. The model is defined by a grid, a width of the individual
    modes and a symmetry group.

    The main task of this object is to compute pole-figures and inverse pole-figures of the
    basis-functions. It provides several different functions for this that are appropriate in
    different settings.

    Parameters:
    -----------
        grid (Rotation list object)
            Positions of the basis functions.
        point_group (odftt.texture.point_groups)
            Rotation objects of the lattice symmetries.
        sigma (float)
            Width of the gaussian basis functions in radians.
    """

    def __init__(self, grid, point_group, sigma=0.1):

        self.rotations = grid
        self.n_modes = len(grid)
        self.g_sym = point_group
        self.coefficients = np.zeros(len(grid))
        self.sigma = sigma
        self.normalization_constant = 4*np.pi/np.sqrt(2*np.pi)/sigma**3
        self.pf_normalization_constant = 1/2*1/np.sqrt(2*np.pi)**2/sigma**2

    def basis_function(self, n, g):
        """ Compute the value of a single basis function at an array of points in
        rotation space.
        Not needed by the reconstruction workflow, but can be used to generate plots.

        Parameters:
        -----------
        n (int)
            index of the basis function
        g (list[Rotation] or Rotation list object)
            The coordinates of g to compute the basis function value at

        Return:
        -------
            numpy array containing the value of the basis function
        """
        g_n_inverse = self.rotations[n].inv()
        odf_value_array = np.zeros(len(g))

        for gs in self.g_sym:
            rotations = g_n_inverse*g*gs
            norms = rotations.magnitude()
            odf_value_array += np.exp(-norms**2/2/self.sigma**2) / len(self.g_sym)

        return odf_value_array * self.normalization_constant

    def evaluate_pfmatrix(self, coordinates, q_hkl):
        """ Compute a matrix of pole-figure values of all basis functions in parallel,
        Called by the main reconstruction worflow to generate the projection matrix.

        Parameters:
        -----------
            coordinates (np.array)
                A 3-dimensional array of shape (N, M, 3) unit-vectors with the q-bin as the
                second index and and the vector index as the last position.

            q_hkl (List[np.array])
                A M-length list of 3-length numpy arrays containging normalized lattice-space
                vectors correspoding to the probed q-vectors. Length must match the second
                index of `coordinates`.
                NOT MILLER INDICIES

        Returns:
        --------
            A 3D containing pole-figure values of all basis function in the input directions.
            the first dimension in the basis function and the last two dinmensions match the
            first two dimensions of the input coordinates. (shape `self.n_modes`, N, M)
        """

        # Back-rotate all probed vectors by grid rotations
        coordinates_flattened = coordinates.reshape((-1, 3))
        q_intermediate = np.stack([rot.inv().apply(coordinates_flattened) for rot in self.rotations], axis=0)
        q_intermediate = q_intermediate.reshape((self.n_modes, coordinates.shape[0], coordinates.shape[1], 3))
        h_vecs_normed = np.stack([h / np.linalg.norm(h) for h in q_hkl], axis=0)
        weights_array = np.zeros((self.n_modes,
                                  coordinates.shape[0],
                                  coordinates.shape[1],))

        # Loop over symmetry equivalent h-vectors
        for gs in self.g_sym:
            h_rot = gs.apply(h_vecs_normed)

            # Take dot product of probed-direction and h-vector
            q_z_fullrot = np.einsum('hi, mchi -> mch', h_rot, q_intermediate)

            # Evaluate gaussian approximately
            gaussian_arg = -(1 - q_z_fullrot) / self.sigma**2
            where_nonzero = gaussian_arg > -6
            weights_array[where_nonzero] += np.exp(gaussian_arg[where_nonzero])
            # Friedel partner
            gaussian_arg = -(1 + q_z_fullrot) / self.sigma**2
            where_nonzero = gaussian_arg > -6
            weights_array[where_nonzero] += np.exp(gaussian_arg[where_nonzero])

        return (weights_array / 2 * (1/2*1/np.sqrt(2*np.pi)**2/self.sigma**2)).reshape((self.n_modes, -1))

    def evaluate_pf(self, n, thetas, phis, q_hkl):
        """ Comput the pole figure values of a single basis function at an unstructured
        list of coordinates.
        Not needed by the reconstruction workflow, but can be used to generate plots.

        Parameters:
        -----------

        n (int)
            index of the basis function
        thetas (1D np.array)
            Theta coordinates of teh points to be evaluated.
        phis (1D np.array)
            Psi coordinates of teh points to be evaluated. Must have same length as `thetas`.
        q_hkl (1D np.array)
            3-length vector containing the normalized lattice-space vector.
            NOT MILLER INDICIES

        Return:
        -------
            numpy array containing the value of the polegifures.
        """
        N_directions = len(thetas)
        x = np.cos(phis)*np.sin(thetas)
        y = np.sin(phis)*np.sin(thetas)
        z = np.cos(thetas)
        directions_vectors = np.stack((x, y, z), axis=-1)

        pf_matrix = np.zeros(N_directions)
        # Positive
        q_norm = np.array(q_hkl) / np.linalg.norm(q_hkl)
        sym_equivalent_qs = np.stack([(self.rotations[n]*gs).apply(q_norm) for gs in self.g_sym], axis=0)

        distances = np.arccos(np.einsum('mi,si->ms', directions_vectors, sym_equivalent_qs))
        pf_matrix += np.sum(np.exp(-distances**2/2/self.sigma**2), axis=-1)

        # Friedel sym version
        sym_equivalent_qs = np.stack([(self.rotations[n]*gs).apply(-q_norm) for gs in self.g_sym], axis=0)

        distances = np.arccos(np.einsum('mi,si->ms', directions_vectors, sym_equivalent_qs))
        pf_matrix += np.sum(np.exp(-distances**2/2/self.sigma**2), axis=-1)

        return pf_matrix / 2 * self.pf_normalization_constant

    def evaluate_ipf(self, n, thetas, phis, dir_vec):
        """ Comput the inverse pole figure values of a single basis function at an unstructured
        list of coordinates.
        Not needed by the reconstruction workflow, but can be used to generate plots.

        Parameters:
        -----------
        n (int)
            index of the basis function
        thetas (1D np.array)
            Theta coordinates of teh points to be evaluated.
        phis (1D np.array)
            Psi coordinates of teh points to be evaluated. Must have same length as `thetas`.
        dir_vec (1D np.array)
            3-length vector containing the normalized sample-space direction

        Return:
        -------
            numpy array containing the value of the inverse polegifures.
        """
        N_directions = len(thetas)
        x = np.cos(phis)*np.sin(thetas)
        y = np.sin(phis)*np.sin(thetas)
        z = np.cos(thetas)
        directions_vectors = np.stack((x, y, z), axis=-1)

        ipf_matrix = np.zeros(N_directions)
        # Positive
        dir_norm = np.array(dir_vec) / np.linalg.norm(dir_vec)
        sym_equivalent_qs = np.stack([(self.rotations[n]*gs).inv().apply(dir_norm)
                                      for gs in self.g_sym], axis=0)
        distances = np.arccos(np.einsum('mi,si->ms', directions_vectors, sym_equivalent_qs))
        ipf_matrix += np.sum(np.exp(-distances**2/2/self.sigma**2), axis=-1)

        # Friedel sym version
        sym_equivalent_qs = np.stack([(self.rotations[n]*gs).inv().apply(-dir_norm)
                                      for gs in self.g_sym], axis=0)
        distances = np.arccos(np.einsum('mi,si->ms', directions_vectors, sym_equivalent_qs))
        ipf_matrix += np.sum(np.exp(-distances**2/2/self.sigma**2), axis=-1)

        return ipf_matrix / 2 * self.pf_normalization_constant

    def compute_polefigure_matrix(self, args_tuple):
        """ Use to simplify the mutiprocessing code in `compute_polefigure_matrices_parallel`.
        """
        basisfunctions_matrix = self.evaluate_pfmatrix(args_tuple[0], args_tuple[1])
        return basisfunctions_matrix

    def compute_polefigure_matrices_parallel(self, coordinates, h_vectors, num_processes,
                                             make_sparse=False, cutoff_value=0.05, print_progress=False):
        print('Starting parallel computation of polefiugres.\n')
        t_start = time.time()
        basisfunctions = []
        with Pool(num_processes) as pool:

            iterable_args = (
                (coordinates[rotation_index, 0, 0], h_vectors)
                for rotation_index in range(coordinates.shape[0])
            )

            num_done = 0
            next_frac = 0.0
            for result in pool.imap(self.compute_polefigure_matrix, iterable_args):

                basisfunction_array_thisrotation = result.reshape((self.n_modes, -1))

                if make_sparse:
                    under_threshold = basisfunction_array_thisrotation\
                        < cutoff_value*self.pf_normalization_constant
                    basisfunction_array_thisrotation[under_threshold] = 0.0
                    basisfunctions.append(csr_array(basisfunction_array_thisrotation))
                else:
                    basisfunctions.append(basisfunction_array_thisrotation)

                if print_progress:
                    # quick progress tracker
                    num_done += 1
                    percent_increm = 1
                    if num_done / coordinates.shape[0] > next_frac:
                        t_event = time.time()
                        if next_frac == 0.0 and t_event-t_start < 1:
                            percent_increm = 10

                        delta = timedelta(seconds=t_event-t_start)
                        print(f'\r{next_frac*100:.0f}% done. Time elapsed: {delta}')
                        next_frac += percent_increm/100

        return basisfunctions

    def make_polefigure_map(self, coefficients, lattice_direction, resolution_in_degrees=2):
        """ Make a latitude-longitude map of a single polefigure suitible for plotting.
        Parameters:
        -----------
            coefficients (numpy array[float])
                Length `grid_size**3` 1D-array containing the coefficients of the ODF.

            lattice_direction (numpy array[float])
                1D array of length 3. UNit vector descibing the lattice-space direction
                to compute the pole-figure in.

            resolution_in_degrees (float)
                Resolution of the desired poelfigure map.

        Returns:
        --------
            polefigure_map (numpy array[float])
                latitude longitude map of the computed polefigure.

            theta_grid (numpy array[float])
                Polar angle in radians. Same shape as polefigure_map.

            phi_grid (numpy array[float])
                Azimuthal angle in radians. Same shape as polefigure_map.
        """
        # Make grid
        theta_grid = np.linspace(0, np.pi/2, int(90/resolution_in_degrees+1), endpoint=True)
        phi_grid = np.linspace(0, 2*np.pi, int(360/resolution_in_degrees+1), endpoint=True)
        theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

        # Initialize polefigure map
        mapshape = theta_grid.shape
        polefigure_map = np.zeros(mapshape)

        # Normalize lattice direction to be safe
        lattice_direction = lattice_direction / np.linalg.norm(lattice_direction)

        nonzero_modes = np.arange(self.n_modes)[coefficients != 0]
        for modenumber in nonzero_modes:
            polefigure_map[...] += self.evaluate_pf(modenumber, theta_grid.ravel(),
                                                    phi_grid.ravel(), lattice_direction)\
                                                        .reshape(mapshape)*coefficients[modenumber]

        return polefigure_map, theta_grid, phi_grid

    def make_inverse_polefigure_map(self, coefficients, realspace_direction, resolution_in_degrees=2):
        """ Make a latitude-longitude map of a single inverse polefigure suitible for plotting.
        Parameters:
        -----------
            coefficients (numpy array[float])
                Length `grid_size**3` 1D-array containing the coefficients of the ODF.

            realspace_direction (numpy array[float])
                1D array of length 3. Unit vector descibing the sample-space direction
                to compute the invere pole-figure in.

            resolution_in_degrees (float)
                Resolution of the desired inverse pole figure.

        Returns:
        --------
            inverse_polefigure_map (numpy array[float])
                latitude longitude map of the computed inverse pole figure.

            theta_grid (numpy array[float])
                Polar angle in radians. Same shape as `inverse_polefigure_map`.

            phi_grid (numpy array[float])
                Azimuthal angle in radians. Same shape as `inverse_polefigure_map`.
        """

        # Make grid
        theta_grid = np.linspace(0, np.pi/2, int(90/resolution_in_degrees+1), endpoint=True)
        phi_grid = np.linspace(0, 2*np.pi, int(360/resolution_in_degrees+1), endpoint=True)
        theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

        # Initialize polefigure map
        mapshape = theta_grid.shape
        inverse_polefigure_map = np.zeros(mapshape)

        # Normalize lattice direction to be safe
        realspace_direction = realspace_direction / np.linalg.norm(realspace_direction)

        nonzero_modes = np.arange(self.n_modes)[coefficients != 0]
        for modenumber in nonzero_modes:
            inverse_polefigure_map[...] += self.evaluate_ipf(modenumber, theta_grid.ravel(),
                                                             phi_grid.ravel(), realspace_direction)\
                                                                .reshape(mapshape)*coefficients[modenumber]

        return inverse_polefigure_map, theta_grid, phi_grid
