import numpy as np
from mumott.core.wigner_d_utilities import load_d_matrices
from odftt.spharm.spharm_tools import spharm_values_single_ell_unstructured_coords
from odftt.spharm import map_from_spharm_coefficients


class Harmonics:
    """ Abstract representation of a generalized spherical harmonics based model of an Orientation
    Distribution Function (ODF). The model is defined by a list of symmetrized modes, containing the (real)
    spherical harmonics coefficients of the symmetrized surface harmonics of a given symmetry group.
    Sample-symmetries are not enforced.

    This model uses the same definition of the spherical harmonics and Wigner's D matrices as `mumott`.
    Note in particular that we use purely real harmonics! The spherical harmonics are ordered with first
    the sine- harmonics in descending order, then the cosine harmonics in ascending order. I.e:

    Index, ell, |m|, Parity (wrt. to mirror in (x-z) plane)
    ---------------------
    0      0     0   Even
    1      2     2   Odd (i.e sine)
    2      2     1   Odd
    3      2     0   Even
    4      2     1   Even (i.e cosine)
    5      2     2   Even
    6      4     4   Odd
    7      4     3   Odd
    8      4     2   Odd
    9      4     1   Odd
    10     4     0   Even
    11     4     1   Even
    ... and so on.

    This is ofc. because it looks like the complex-ordering, but negative m makes no sense for the reals!

    Odd-ell harmonics are always omitted and generalized spherical harmonics coefficients are represented by
    (2*ell+1) times (2*ell+1) matrices with the same ordering as the spharms. along each dimension.

    The main task of this object is to compute pole-figures and inverse pole-figures of the basis-functions.
    It provides several different functions for this that are appropriate in differnt settings.

    Parameters:
    -----------
        ell_max (int)
            Band limit of the model.
        symmetrized_mode_coefficients (list(dict))
            List of symmetrized surface harmonics containing their order 'ell'
            and their coefficients 'coeff'.
            If no input is given, it will assume  no symmetry (triclinic). (probably not what you want)
    """

    def __init__(self, ell_max, symmetrized_mode_coefficients=None):

        self.ell_max = ell_max
        self.d_matrices = load_d_matrices(ell_max)
        self.mode_coefficients = []
        if symmetrized_mode_coefficients is not None:
            for mode in symmetrized_mode_coefficients:
                ell = mode['ell']
                if ell > ell_max:
                    break
                for n in range(-ell, ell+1):
                    coeffs = np.zeros((2*ell+1, 2*ell+1))
                    coeffs[:, n+ell] = mode['coeffs']
                    self.mode_coefficients.append({'ell': ell, 'coeffs': coeffs})

        else:
            for ell in range(0, ell_max + 2, 2):
                for m in range(-ell, ell+1):
                    for n in range(-ell, ell+1):
                        coeffs = np.zeros((2*ell+1, 2*ell+1))
                        coeffs[m+ell, n+ell] = 1
                        self.mode_coefficients.append({'ell': ell, 'coeffs': coeffs})

        self.n_modes = len(self.mode_coefficients)

    def get_mode_pole_figure_coeffs(self, modenumber, lattice_space_vector):
        """ Get the spharm coefficients of the pole figure of a specific basis function.

        Parameters:
        -----------
        modenumber (int)
            Index of the basis function to be computed.

        lattice_space_vector (np.array)
            Lattice space direction to compute pole figure in (xyz). NOT MILLER INDICIES

        Returns:
        --------
            spherical harmonics coefficients of the pole figure. Only at the specific `ell.`
        """
        h = lattice_space_vector / np.linalg.norm(lattice_space_vector)
        theta_h = np.arccos(h[2])
        phi_h = np.arctan2(h[1], h[0])

        ell = self.mode_coefficients[modenumber]['ell']
        mphi = (np.arange(-ell, ell+1) * phi_h)[np.newaxis, :]
        mtheta = (np.arange(-ell, ell+1) * theta_h)[np.newaxis, :]
        normalization = 1 / np.sqrt(2*ell + 1)

        gsh_coeffs = np.copy(self.mode_coefficients[modenumber]['coeffs']).T
        gsh_coeffs = gsh_coeffs[::1, :] * np.cos(mphi) - gsh_coeffs[:, ::-1] * np.sin(mphi)
        gsh_coeffs = gsh_coeffs @ self.d_matrices[ell]
        gsh_coeffs = gsh_coeffs[::1, :] * np.cos(mtheta) - gsh_coeffs[:, ::-1] * np.sin(mtheta)
        gsh_coeffs = gsh_coeffs @ self.d_matrices[ell].T

        sph_coeffs = normalization * gsh_coeffs[:, ell]
        return sph_coeffs

    def get_mode_inverse_pole_figure_coeffs(self, modenumber, sample_space_vector):
        """ Get the spharm coefficients of the inverse pole figure of a specific basis function.

        Parameters:
        -----------
        modenumber (int)
            Index of the basis function to be computed.

        sample_space_vector (np.array)
            Sample space direction to compute pole figure in (xyz).

        Returns:
        --------
            spherical harmonics coefficients of the inverse pole figure. Only at the specific `ell.`
        """
        y = sample_space_vector / np.linalg.norm(sample_space_vector)
        theta_y = np.arccos(y[2])
        phi_y = np.arctan2(y[1], y[0])

        ell = self.mode_coefficients[modenumber]['ell']
        mphi = (np.arange(-ell, ell+1) * phi_y)[np.newaxis, :]
        mtheta = (np.arange(-ell, ell+1) * theta_y)[np.newaxis, :]
        normalization = 1 / np.sqrt(2*ell+1)

        gsh_coeffs = np.copy(self.mode_coefficients[modenumber]['coeffs'])
        gsh_coeffs = gsh_coeffs[::1, :] * np.cos(mphi) + gsh_coeffs[:, ::-1] * np.sin(mphi)
        gsh_coeffs = gsh_coeffs @ self.d_matrices[ell].T
        gsh_coeffs = gsh_coeffs[::1, :] * np.cos(mtheta) + gsh_coeffs[:, ::-1] * np.sin(mtheta)
        gsh_coeffs = gsh_coeffs @ self.d_matrices[ell]

        sph_coeffs = normalization * gsh_coeffs[:, ell]
        return sph_coeffs

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
        weights_array = np.zeros((len(self.mode_coefficients),
                                  coordinates.shape[0],
                                  coordinates.shape[1],))

        for h_index, hkl in enumerate(q_hkl):

            q_sample_space = coordinates[:, h_index, :]
            theta = np.arccos(q_sample_space[..., 2]).flatten()
            phi = np.arctan2(q_sample_space[..., 1], q_sample_space[..., 0]).flatten()

            ell = -1
            for modenumber in range(self.n_modes):

                new_ell = self.mode_coefficients[modenumber]['ell']

                if new_ell != ell:
                    ell = new_ell
                    spharm_values = spharm_values_single_ell_unstructured_coords(ell, theta, phi)
                    spharm_values = spharm_values.reshape((*q_sample_space.shape[:-1], 2*ell+1))

                coeffs = self.get_mode_pole_figure_coeffs(modenumber, hkl)
                weights_array[modenumber, :, h_index] = np.einsum('im,m->i', spharm_values, coeffs)

        return weights_array.reshape((self.n_modes, -1))

    def get_pole_figure_coeffs(self, symmetrized_gsh_coeffs, lattice_space_vector):
        """ Get the spharm coefficients of the pole figure of the full model with the
        given symmetrized mode coefficients.

        Parameters:
        -----------
        symmetrized_gsh_coeffs (np.array)
            Symmetrized mode coefficients of the full odf.

        lattice_space_vector (np.array)
            Lattice space direction to compute pole figure in (xyz). NOT MILLER INDICIES

        Returns:
        --------
            spherical harmonics coefficients of the pole figure.
        """

        spharm_coeffs = np.zeros((self.ell_max + 1)*(self.ell_max + 2)//2)
        for modenumber in range(self.n_modes):
            ell = self.mode_coefficients[modenumber]['ell']
            if ell == 0:
                slc = slice(0, 1)
            else:
                slc = slice(ell*(ell - 1)//2, (ell + 1)*(ell + 2)//2)

            spharm_coeffs[slc] += self.get_mode_pole_figure_coeffs(modenumber, lattice_space_vector)\
                * symmetrized_gsh_coeffs[modenumber]

        return spharm_coeffs

    def get_inverse_pole_figure_coeffs(self, symmetrized_gsh_coeffs, sample_space_vector):
        """ Get the spharm coefficients of the inverse pole figure of the full model with the
        given symmetrized mode coefficients.

        Parameters:
        -----------
        symmetrized_gsh_coeffs (np.array)
            Symmetrized mode coefficients of the full odf.

        sample_space_vector (np.array)
            Sample space direction to compute pole figure in (xyz).

        Returns:
        --------
            spherical harmonics coefficients of the inverse pole figure.
        """
        spharm_coeffs = np.zeros((self.ell_max + 1)*(self.ell_max + 2)//2)
        for modenumber in range(self.n_modes):
            ell = self.mode_coefficients[modenumber]['ell']
            if ell == 0:
                slc = slice(0, 1)
            else:
                slc = slice(ell*(ell - 1)//2, (ell + 1)*(ell + 2)//2)

            spharm_coeffs[slc] += self.get_mode_inverse_pole_figure_coeffs(modenumber, sample_space_vector)\
                * symmetrized_gsh_coeffs[modenumber]

        return spharm_coeffs

    def make_GSH_coeffs(self, sym_coeffs):
        """ Routine to convert symmetrized harmonics coefficients into GSH coefficients in the full basis.

        Parameters:
        -----------
        sym_coeffs
            Sequence of length `self.n_modes` containing the symmetrized coefficients to be converted.

        Returns:
        --------
        GSH_coeffs
            List of length `self.ell_max + 1` where the `ell`th element is a `(2*ell+1)` times `(2*ell+1)`
            array containgin the GSH coefficients of order `ell`. Odd orders will be included but equal zero.
        """

        GSH_coeffs = []

        for ell in range(0, self.ell_max + 1):
            GSH_coeffs.append(np.zeros((2*ell + 1, 2*ell + 1)))

        for ii, mode in enumerate(self.mode_coefficients):

            ell = mode['ell']
            GSH_coeffs[ell] += sym_coeffs[ii] * mode['coeffs']

        return GSH_coeffs

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
                Resolution of the desired pole figure map.

        Returns:
        --------
            polefigure_map (numpy array[float])
                latitude longitude map of the computed polefigure.

            theta_grid (numpy array[float])
                Polar angle in radians. Same shape as polefigure_map.

            phi_grid (numpy array[float])
                Azimuthal angle in radians. Same shape as polefigure_map.
        """
        # Normalize lattice direction to be safe
        lattice_direction = np.array(lattice_direction) / np.linalg.norm(lattice_direction)

        pf_sph_coeffs = self.get_pole_figure_coeffs(coefficients, lattice_direction)

        # Make grid
        theta_values = np.linspace(0, np.pi/2, int(90/resolution_in_degrees+1), endpoint=True)
        phi_values = np.linspace(0, 2*np.pi, int(360/resolution_in_degrees+1), endpoint=True)
        pf_values = map_from_spharm_coefficients(self.ell_max, pf_sph_coeffs, theta_values, phi_values)

        theta_grid, phi_grid = np.meshgrid(theta_values, phi_values, indexing='ij')

        return pf_values, theta_grid, phi_grid

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
        # Normalize lattice direction to be safe
        realspace_direction = np.array(realspace_direction) / np.linalg.norm(realspace_direction)

        ipf_sph_coeffs = self.get_inverse_pole_figure_coeffs(coefficients, realspace_direction)

        # Make grid
        theta_values = np.linspace(0, np.pi/2, int(90/resolution_in_degrees+1), endpoint=True)
        phi_values = np.linspace(0, 2*np.pi, int(360/resolution_in_degrees+1), endpoint=True)
        ipf_values = map_from_spharm_coefficients(self.ell_max, ipf_sph_coeffs, theta_values, phi_values)

        theta_grid, phi_grid = np.meshgrid(theta_values, phi_values, indexing='ij')

        return ipf_values, theta_grid, phi_grid
