import numpy as np
from scipy.spatial.transform import Rotation as R
import numba
from math import floor


class SingleGrain:
    """ Representation of a grid-based model of an Orientation Distribution Function (ODF)
    that constist of a voxelization of a tangent-space centered on `average_orientation`.

    Supposed to be used in conjunction with `tomography_models.on_the_fly_model` to do
    single grain reconstructions or sum-of-grains reconstructions.

    Parameters:
    -----------
        average_orientation (single Rotation object)
            Point in orientation space on which the grid is centered.
        orientation_range (float)
            Range of orientation (in randians) that the grid will cover. (half edge length)
        grid_size (int)
            Number of grid points in each dimension. The total number of orientations in the
            grid will be `grid_size**3`.
        point_group (odftt.texture.point_groups)
            Rotation objects of the lattice symmetries. Only used to compute pole-figures
            and inverse pole figures. The grid itself does not respect lattice symmetries.
    """

    def __init__(self, average_orientation, orientation_range, grid_size, point_group):

        self.grid_size = grid_size
        self.average_orientation = average_orientation
        self.orientation_range = orientation_range
        self.g_sym = point_group
        self.step_size = 2 * orientation_range / (grid_size-1)

    def rotation_grid(self):
        """ Method to return the grid of orientations in a format useable by other functions.

        Returns:
        --------
            grid (Rotation list object)
                List of orientations of length `grid_size**3` containging the full oritentations
                of the grid.
        """

        x = np.linspace(-self.orientation_range, self.orientation_range, self.grid_size)
        x, y, z = np.meshgrid(x, x, x, indexing='ij')
        grid = R.from_rotvec(np.stack([x.ravel(), y.ravel(), z.ravel()], axis=-1)) * self.average_orientation
        return grid

    def projection(self, coefficients, coordinates, h_vectors):
        """ Compute the pole-figure transform of the ODFs with coefficients `coefficients` at the points
        specified by `h_vectors` and `coordinates`.

        Suposed to work well in a setting where only a few hkls are given but many lab-space directions.

        The lab-space directions can be different for the differnt hkl-directions (as is the case
        experimentally).

        Parameters:
        -----------
            coefficients (numpy array[float])
                2D array containging the coefficients of the ODFs to be computed on.
                First dimension is the number of ODF being operated on (Nr normally one for each voxel).
                The second dimension numbers the grid points and must be of length `grid_size**3`.

            coordinates (numpy array[float])
                3D numpy array containgin unit-3-vectors of the laboratory space directions where
                the pole-figure transforms are to be computed.
                The first dimension numbers the real-space directions. (Ny)
                The second dimension numbers the different hkl-directions. (Nh)
                The third dimension is the vector index and must be of length 3.

            h_vectors (list[numpy array[float]])
                List of hkl vectors to be calculated. The list muct be of length (n_hkl).
                The arrays contained in `h_vectors` must be of length 3.

        Returns:
        --------
            output_array (numpy array[float])
                Pole-figure transform of the given ODFs.
                Shape is [Nr, Ny, Nh].
        """

        oldshape = coefficients.shape
        coefficients = coefficients.reshape((-1, self.grid_size, self.grid_size, self.grid_size))
        output_array = np.zeros((coefficients.shape[0], *coordinates.shape[:2]))
        n_hkl = len(h_vectors)

        average_orientation_mat = self.average_orientation.as_matrix()
        symmetry_matrices = np.stack([sym.as_matrix() for sym in self.g_sym], axis=0)

        for hkl_index in range(n_hkl):

            h = h_vectors[hkl_index]
            h = h / np.linalg.norm(h)

            for sym in symmetry_matrices:

                hg = average_orientation_mat @ sym @ h
                offsets = np.cross(hg, coordinates[:, hkl_index, :])\
                    / np.dot(hg, coordinates[:, hkl_index, :].T)[:, np.newaxis]
                offset_norm = np.linalg.norm(offsets, axis=1)

                for azim_index in np.arange(coordinates.shape[0])[offset_norm < (self.orientation_range * 2)]:
                    proj_val = projection_single_ray(hg, offsets[azim_index, :]/self.step_size,
                                                     coefficients, np.array([self.grid_size]*3, dtype=int))
                    output_array[:, azim_index, hkl_index] += proj_val

        coefficients = coefficients.reshape(oldshape)
        return output_array

    def adjoint(self, intensities, coordinates, h_vectors):
        """ Compute the adjointy of the pole-figure transform of the ODFs with coefficients `coefficients`
        at the points specified by `h_vectors` and `coordinates`.

        NOTE: Be aware this has nothing to do with inverse pole figures! Those should also be computed
        with `SingleGrain.projection`. `SingleGrain.make_inverse_polefigure_map` provides a convenient
        wrapper.

        Suposed to work well in a setting where only a few hkls are given but many lab-space directions.

        The lab-space directions can be different for the differnt hkl-directions (as is the case
        experimentally).

        Parameters:
        -----------
            intensities (numpy array[float])
                3D array containging the pole-figure values measured.
                First dimension is the number of diffraction patterns being operated on (Nj, normally one for
                each point in the raster-scan).
                The second dimension number of directions measured for each hkl order. (Ny)
                The third is the number of hkl orders being measured (n_hkl).

            coordinates (numpy array[float])
                3D numpy array containgin unit-3-vectors of the laboratory space directions where
                the adjoint pole-figure transforms are to be computed.
                The first dimension numbers the real-space directions. (Ny)
                The second dimension numbers the different hkl-directions. (n_hkl)
                The third dimension is the vector index and must be of length 3.

            h_vectors (list[numpy array[float]])
                List of hkl vectors to be calculated. The list must be of length (n_hkl).
                The arrays contained in `h_vectors` must be of length 3.and

        Returns:
        --------
            output_array (numpy array[float])
                Adjoint of pole-figure transform of the given ODFs.
                Shape is [Nr, `grid_size**3`].
        """
        oldshape = intensities.shape
        det_channels_shape = coordinates.shape[:-1]  # (Ny, Nh)
        intensities = intensities.reshape((-1, *det_channels_shape))
        output_coefficients = np.zeros((intensities.shape[0], self.grid_size, self.grid_size, self.grid_size))
        n_hkl = len(h_vectors)

        average_orientation_mat = self.average_orientation.as_matrix()
        symmetry_matrices = [sym.as_matrix() for sym in self.g_sym]

        for hkl_index in range(n_hkl):

            h = h_vectors[hkl_index]
            h = h / np.linalg.norm(h)

            for sym in symmetry_matrices:
                hg = average_orientation_mat @ sym @ h
                offsets = np.cross(hg, coordinates[:, hkl_index, :])\
                    / np.dot(hg, coordinates[:, hkl_index, :].T)[:, np.newaxis]
                offset_norm = np.linalg.norm(offsets, axis=1)

                for azim_index in np.arange(coordinates.shape[0])[offset_norm < (self.orientation_range * 2)]:
                    backprojection_single_ray(hg, offsets[azim_index, :] / self.step_size,
                                              output_coefficients, np.array([self.grid_size]*3, dtype=int),
                                              intensities[:, azim_index, hkl_index])

        intensities = intensities.reshape(oldshape)
        return output_coefficients.reshape((intensities.shape[0], self.grid_size**3))

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
                Resolution of the desired poelfigure map.__annotations__

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

        coordinates = np.stack([
            np.sin(theta_grid) * np.cos(phi_grid),
            np.sin(theta_grid) * np.sin(phi_grid),
            np.cos(theta_grid),
        ], axis=-1).reshape(-1, 3)[:, np.newaxis, :]  # Add empty dimension to number hkls

        # Compute polefigure map
        mapshape = theta_grid.shape
        polefigure_map = self.projection(coefficients[np.newaxis, :],
                                         coordinates, [lattice_direction])[0, :, 0].reshape(mapshape)
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

        # WARNING: Super inefficients because the loop over directions happens in c-python.
        # this could be improved significanlty by a dedicated implemenation of self.projection.

        # Make grid
        theta_grid = np.linspace(0, np.pi/2, int(90/resolution_in_degrees+1), endpoint=True)
        phi_grid = np.linspace(0, 2*np.pi, int(360/resolution_in_degrees+1), endpoint=True)
        theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

        coordinates = np.stack([
            np.sin(theta_grid) * np.cos(phi_grid),
            np.sin(theta_grid) * np.sin(phi_grid),
            np.cos(theta_grid),
        ], axis=-1).reshape(-1, 3)

        lattice_direction = [coordinates[index, :] for index in range(coordinates.shape[0])]
        realspace_direction = np.repeat(np.array(realspace_direction)[np.newaxis, np.newaxis, :],
                                        coordinates.shape[0], 1)

        # Compute polefigure map
        mapshape = theta_grid.shape
        polefigure_map = self.projection(coefficients[np.newaxis, :],
                                         realspace_direction, lattice_direction)[0, 0, :].reshape(mapshape)
        return polefigure_map, theta_grid, phi_grid


@numba.njit()
def projection_single_ray(direction, offset_vector, density_array, volume_shape):
    """
    Do a single backprojection with the slice-by-slice bi-linear scheme.
    This is only an approximate adjoint of the projeciton used in this file.
    """
    #  Figure out what is the fast direction for a given projection.
    if abs(direction[0]) >= max(abs(direction[1]), abs(direction[2])):
        fast_direction = 0
    elif abs(direction[1]) > max(abs(direction[0]), abs(direction[2])):
        fast_direction = 1
    else:
        fast_direction = 2

    # Always project in posiive direction
    if direction[fast_direction] < 0:
        direction = -direction

    increment = (direction[0]/abs(direction[fast_direction]),
                 direction[1]/abs(direction[fast_direction]),
                 direction[2]/abs(direction[fast_direction]))

    sec = 1/abs(direction[fast_direction])

    # Position of center in voxel coords
    P_x = volume_shape[0]/2 - 0.5
    P_y = volume_shape[1]/2 - 0.5
    P_z = volume_shape[2]/2 - 0.5

    # Init. accumulator
    cum_sum = np.zeros(density_array.shape[0])

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 0:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[1] - increment[1]*(volume_shape[0]/2-0.5 + offset_vector[0]) + P_y,
               offset_vector[2] - increment[2]*(volume_shape[0]/2-0.5 + offset_vector[0]) + P_z,)

        # Loop over slices
        for x in range(0, volume_shape[0]):

            y = floor(pos[0])
            yfrac = pos[0] % 1
            z = floor(pos[1])
            zfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if y >= 0 and y < volume_shape[1]:
                if z >= 0 and z < volume_shape[2]:
                    cum_sum[:] += sec*(1-yfrac)*(1-zfrac)*density_array[:, x, y, z]
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    cum_sum[:] += sec*(1-yfrac)*zfrac*density_array[:, x, y, z+1]
            if y+1 >= 0 and y+1 < volume_shape[1]:
                if z >= 0 and z < volume_shape[2]:
                    cum_sum[:] += sec*yfrac*(1-zfrac)*density_array[:, x, y+1, z]
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    cum_sum[:] += sec*yfrac*zfrac*density_array[:, x, y+1, z+1]

            pos = (pos[0] + increment[1], pos[1] + increment[2])

        return cum_sum

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 1:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[0] - increment[0]*(volume_shape[1]/2-0.5 + offset_vector[1]) + P_x,
               offset_vector[2] - increment[2]*(volume_shape[1]/2-0.5 + offset_vector[1]) + P_z,)

        # Loop over slices
        for y in range(0, volume_shape[1]):

            x = floor(pos[0])
            xfrac = pos[0] % 1
            z = floor(pos[1])
            zfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if x >= 0 and x < volume_shape[0]:
                if z >= 0 and z < volume_shape[2]:
                    cum_sum[:] += sec*(1-xfrac)*(1-zfrac)*density_array[:, x, y, z]
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    cum_sum[:] += sec*(1-xfrac)*zfrac*density_array[:, x, y, z+1]
            if x+1 >= 0 and x+1 < volume_shape[0]:
                if z >= 0 and z < volume_shape[2]:
                    cum_sum[:] += sec*xfrac*(1-zfrac)*density_array[:, x+1, y, z]
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    cum_sum[:] += sec*xfrac*zfrac*density_array[:, x+1, y, z+1]

            pos = (pos[0] + increment[0], pos[1] + increment[2])

        return cum_sum

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 2:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[0] - increment[0]*(volume_shape[2]/2-0.5 + offset_vector[2]) + P_x,
               offset_vector[1] - increment[1]*(volume_shape[2]/2-0.5 + offset_vector[2]) + P_y,)

        # Loop over slices
        for z in range(0, volume_shape[2]):

            x = floor(pos[0])
            xfrac = pos[0] % 1
            y = floor(pos[1])
            yfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if x >= 0 and x < volume_shape[0]:
                if y >= 0 and y < volume_shape[1]:
                    cum_sum[:] += sec*(1-xfrac)*(1-yfrac)*density_array[:, x, y, z]
                if y+1 >= 0 and y+1 < volume_shape[1]:
                    cum_sum[:] += sec*(1-xfrac)*yfrac*density_array[:, x, y+1, z]
            if x+1 >= 0 and x+1 < volume_shape[0]:
                if y >= 0 and y < volume_shape[1]:
                    cum_sum[:] += sec*xfrac*(1-yfrac)*density_array[:, x+1, y, z]
                if y+1 >= 0 and y+1 < volume_shape[1]:
                    cum_sum[:] += sec*xfrac*yfrac*density_array[:, x+1, y+1, z]

            pos = (pos[0] + increment[0], pos[1] + increment[1])

        return cum_sum


@numba.njit()
def backprojection_single_ray(direction, offset_vector, output_array, volume_shape, intensities):
    """
    Do a single backprojection with the slice-by-slice bi-linear scheme.
    This is only an approximate adjoint of the projeciton used in this file.
    """
    #  Figure out what is the fast direction for a given projection.
    if abs(direction[0]) >= max(abs(direction[1]), abs(direction[2])):
        fast_direction = 0
    elif abs(direction[1]) > max(abs(direction[0]), abs(direction[2])):
        fast_direction = 1
    else:
        fast_direction = 2

    # Always project in posiive direction
    if direction[fast_direction] < 0:
        direction = -direction

    increment = (direction[0]/abs(direction[fast_direction]),
                 direction[1]/abs(direction[fast_direction]),
                 direction[2]/abs(direction[fast_direction]))

    sec = 1/abs(direction[fast_direction])

    # Position of center in voxel coords
    P_x = volume_shape[0]/2 - 0.5
    P_y = volume_shape[1]/2 - 0.5
    P_z = volume_shape[2]/2 - 0.5

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 0:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[1] - increment[1]*(volume_shape[0]/2-0.5 + offset_vector[0]) + P_y,
               offset_vector[2] - increment[2]*(volume_shape[0]/2-0.5 + offset_vector[0]) + P_z,)

        # Loop over slices
        for x in range(0, volume_shape[0]):

            y = floor(pos[0])
            yfrac = pos[0] % 1
            z = floor(pos[1])
            zfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if y >= 0 and y < volume_shape[1]:
                if z >= 0 and z < volume_shape[2]:
                    output_array[:, x, y, z] += sec*(1-yfrac)*(1-zfrac)*intensities
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    output_array[:, x, y, z+1] += sec*(1-yfrac)*zfrac*intensities
            if y+1 >= 0 and y+1 < volume_shape[1]:
                if z >= 0 and z < volume_shape[2]:
                    output_array[:, x, y+1, z] += sec*yfrac*(1-zfrac)*intensities
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    output_array[:, x, y+1, z+1] += sec*yfrac*zfrac*intensities

            pos = (pos[0] + increment[1], pos[1] + increment[2])

        return output_array

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 1:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[0] - increment[0]*(volume_shape[1]/2-0.5 + offset_vector[1]) + P_x,
               offset_vector[2] - increment[2]*(volume_shape[1]/2-0.5 + offset_vector[1]) + P_z,)

        # Loop over slices
        for y in range(0, volume_shape[1]):

            x = floor(pos[0])
            xfrac = pos[0] % 1

            z = floor(pos[1])
            zfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if x >= 0 and x < volume_shape[0]:
                if z >= 0 and z < volume_shape[2]:
                    output_array[:, x, y, z] += sec*(1-xfrac)*(1-zfrac)*intensities
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    output_array[:, x, y, z+1] += sec*(1-xfrac)*zfrac*intensities
            if x+1 >= 0 and x+1 < volume_shape[0]:
                if z >= 0 and z < volume_shape[2]:
                    output_array[:, x+1, y, z] += sec*xfrac*(1-zfrac)*intensities
                if z+1 >= 0 and z+1 < volume_shape[2]:
                    output_array[:, x+1, y, z+1] += sec*xfrac*zfrac*intensities

            pos = (pos[0] + increment[0], pos[1] + increment[2])

        return output_array

    # Handle different fast-directions separately. Six different cases are almost identical.
    if fast_direction == 2:

        # Position of the ray at the entrance sclice in grid coords
        pos = (offset_vector[0] - increment[0]*(volume_shape[2]/2-0.5 + offset_vector[2]) + P_x,
               offset_vector[1] - increment[1]*(volume_shape[2]/2-0.5 + offset_vector[2]) + P_y,)

        # Loop over slices
        for z in range(0, volume_shape[2]):

            x = floor(pos[0])
            xfrac = pos[0] % 1
            y = floor(pos[1])
            yfrac = pos[1] % 1

            # Bi-linear interlpolation with checking that all voxels fall within the array.
            if x >= 0 and x < volume_shape[0]:
                if y >= 0 and y < volume_shape[1]:
                    output_array[:, x, y, z] += sec*(1-xfrac)*(1-yfrac)*intensities
                if y+1 >= 0 and y+1 < volume_shape[1]:
                    output_array[:, x, y+1, z] += sec*(1-xfrac)*yfrac*intensities
            if x+1 >= 0 and x+1 < volume_shape[0]:
                if y >= 0 and y < volume_shape[1]:
                    output_array[:, x+1, y, z] += sec*xfrac*(1-yfrac)*intensities
                if y+1 >= 0 and y+1 < volume_shape[1]:
                    output_array[:, x+1, y+1, z] += sec*xfrac*yfrac*intensities

            pos = (pos[0] + increment[0], pos[1] + increment[1])

        return output_array
