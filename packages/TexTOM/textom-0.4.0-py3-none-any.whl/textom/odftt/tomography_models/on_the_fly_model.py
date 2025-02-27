from mumott.methods.projectors import SAXSProjector as Projector
import numpy as np


class OnTheFlyModel():
    """
    Object responsible for calculating the forward model by composing the pole-figure arrays calculated by
    an  `odftt.texture.odfs` object and computing x-ray transforms on the fly through the methods
    `projection` and `adjoint`. At the moment only compatible with `texture.odfs.SingleGrain`.

    Parameters
    ----------
        odf
            Representation of the ODF model. Probably an object from the `odftt.texture.odfs` submodule.
            Obligatory methods are `odf.n_modes` and 'odf.evaluate_pfmatrix'.

        geom
            `mumott`-style geometry object. only used to initialize the projector object.

        coordinates
            6-D numpy array coontaining q-directions as unit vectors in sample-fixed coordinates.

            Fist index is sample orientation, and and third indexes are unit length.
            Fourth and fifth index are detector azimuth and Bragg-peak index.
            The last index is the vector index and is length 3.

        h_vectors
            List of reciprocal lattice vectors in lattice fixed coordinates. The length of the
            list should match the fifth index of `coordinates`.
            (NOT MILLER INDICIES)
    """

    def __init__(self, odf, geom, coordinates, h_vectors):

        self.odf = odf
        self.h_vectors = h_vectors
        self.n_projections = len(geom)
        self.n_modes = odf.grid_size**3
        self.channels_shape = (len(geom.detector_angles), len(h_vectors))
        self.volume_shape = geom.volume_shape
        self.image_shape = geom.projection_shape
        self.projector = Projector(geom)
        self.coordinates = coordinates

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

        # Project in real-space and reshape output to rotation-by-rotation shape
        proj_coeffs = self.projector.forward(coeffs.astype(self.projector.dtype))\
            .reshape((self.n_projections, np.product(self.image_shape), self.odf.grid_size**3))

        # Loop through rotations and do orientation-space projections
        model_I = np.zeros((self.n_projections, *self.image_shape, *self.channels_shape))
        for ii in range(self.n_projections):
            model_I[ii, ...] = self.odf.projection(proj_coeffs[ii, ...], self.coordinates[ii, 0, 0],
                                                   self.h_vectors)\
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

        # Loop throug rotations and compute orientation-space backprojection
        modes = np.zeros((self.n_projections, np.product(self.image_shape), self.odf.grid_size**3))
        matrix_shape = (np.product(self.image_shape), np.product(self.channels_shape))
        for ii in range(self.n_projections):
            modes[ii, ...] = self.odf.adjoint(residual[ii, ...].reshape(matrix_shape),
                                              self.coordinates[ii, 0, 0],
                                              self.h_vectors)

        # Reshaope to sinogram-shape and do rel-space backprojection
        modes = modes.reshape((self.n_projections, *self.image_shape, self.odf.grid_size**3))
        coeffs = self.projector.adjoint(modes.astype(self.projector.dtype))

        return coeffs
