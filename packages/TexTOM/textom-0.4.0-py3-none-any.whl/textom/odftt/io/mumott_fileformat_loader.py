from mumott.data_handling import DataContainer
try:
    from mumott.core.geometry import GeometryTuple, Geometry
except ModuleNotFoundError:
    try:
        from mumott.data_handling.geometry import GeometryTuple, Geometry
    except ModuleNotFoundError:
        raise ModuleNotFoundError
import numpy as np


def load_series(filenames):
    """ Load a series of mumott format data files from the same sample containing different Bragg peaks.
    """
    # Initialize all the structures I need
    data_arrays = []
    coordinates = []
    weights_arrays = []

    # Use mumott loader to parse the geometry information, to make sure that I am using the same
    # conventions for everything.
    for ii, filename in enumerate(filenames):
        data_container = DataContainer(data_path=filename, data_type='h5')
        geom = data_container.geometry
        coordinates.append(get_probed_coordinates(geom)[:, :, 0, :])
        data_arrays.append(np.array(data_container.data / data_container.diode[:, :, :, np.newaxis]))
        weights_arrays.append(data_container.weights)

    data_array = np.stack(data_arrays, axis=-1)
    weights_arrays = np.stack(weights_arrays, axis=-1)
    coordinates = np.stack(coordinates, axis=-1)

    # Transpose coordinates to a format matching the two other arrays
    coordinates = coordinates.transpose((0, 1, 3, 2))[:, np.newaxis, np.newaxis, :, :]

    return data_array, weights_arrays, coordinates, geom


def get_probed_coordinates(geom, integration_samples=1, full_circle_covered=True):
    """ Calculates and returns the probed polar and azimuthal coordinates on the unit sphere at
    each angle of projection and for each detector segment in the system's geometry.
    """
    n_proj = len(geom)
    n_seg = len(geom.detector_angles)
    probed_directions_zero_rot = np.zeros((n_seg, integration_samples, 3))
    # Impose symmetry if needed.
    if not full_circle_covered:
        shift = np.pi
    else:
        shift = 0
    det_bin_middles_extended = np.copy(geom.detector_angles)
    det_bin_middles_extended = np.insert(det_bin_middles_extended, 0, det_bin_middles_extended[-1] + shift)
    det_bin_middles_extended = np.append(det_bin_middles_extended, det_bin_middles_extended[1] + shift)

    for ii in range(n_seg):

        # Check if the interval from the previous to the next bin goes over the -pi +pi discontinuity
        before = det_bin_middles_extended[ii]
        now = det_bin_middles_extended[ii + 1]
        after = det_bin_middles_extended[ii + 2]

        if abs(before - now + 2 * np.pi) < abs(before - now):
            before = before + 2 * np.pi
        elif abs(before - now - 2 * np.pi) < abs(before - now):
            before = before - 2 * np.pi

        if abs(now - after + 2 * np.pi) < abs(now - after):
            after = after - 2 * np.pi
        elif abs(now - after - 2 * np.pi) < abs(now - after):
            after = after + 2 * np.pi

        # Generate a linearly spaced set of angles covering the detector segment
        start = 0.5 * (before + now)
        end = 0.5 * (now + after)
        inc = (end - start) / integration_samples
        angles = np.linspace(start + inc / 2, end - inc / 2, integration_samples)

        # Make the zero-rotation-frame vectors corresponding to the given angles
        probed_directions_zero_rot[ii, :, :] = np.cos(angles[:, np.newaxis]) * \
            geom.detector_direction_origin[np.newaxis, :]

        probed_directions_zero_rot[ii, :, :] += np.sin(angles[:, np.newaxis]) * \
            geom.detector_direction_positive_90[np.newaxis, :]

    twothetahalf = geom.two_theta / 2
    probed_directions_zero_rot = probed_directions_zero_rot * np.cos(twothetahalf)\
        - np.sin(twothetahalf) * geom.p_direction_0

    # Initialize array for vectors
    probed_direction_vectors = np.zeros((n_proj, n_seg, integration_samples, 3), dtype=np.float64)
    # Calculate all the rotations
    probed_direction_vectors[...] = \
        np.einsum('kij,mli->kmlj', geom.rotations_as_array, probed_directions_zero_rot)

    return probed_direction_vectors


def slice_geometry(geom, slice):
    """ From a mumott geometry object, create a copy containing only a subset of the projections.
    Mainly used to take out the zero-tilt part of a 3D data set.
    """
    newgeom = Geometry()
    newgeom.p_direction_0 = geom.p_direction_0
    newgeom.j_direction_0 = geom.j_direction_0
    newgeom.k_direction_0 = geom.k_direction_0

    newgeom.detector_direction_origin = geom.detector_direction_origin
    newgeom.detector_direction_positive_90 = geom.detector_direction_positive_90

    newgeom.projection_shape = geom.projection_shape
    newgeom.volume_shape = geom.volume_shape
    newgeom.detector_angles = geom.detector_angles

    indicies = range(len(geom))[slice]
    for ii in indicies:
        geom_tp = GeometryTuple(rotation=geom.rotations[ii],
                                j_offset=geom.j_offsets[ii],
                                k_offset=geom.k_offsets[ii],)
        newgeom.append(geom_tp)

    return newgeom
