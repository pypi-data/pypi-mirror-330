from mumott import Geometry
from mumott.core.geometry import GeometryTuple
import numpy as np


def Ry(angle):
    R = np.array([[np.cos(angle), 0, np.sin(angle)],
                 [0, 1, 0],
                 [-np.sin(angle), 0, np.cos(angle)]])
    return R


def make_2D_mumott_geometry(number_of_points, rot_angles, azim_angles, offcen_length=0, tomo_shape=None):
    """ For a simple 2D geometry, we can construct a `mumott.geometry` object from which
    a projector can be created.
    """

    if tomo_shape is None:
        tomo_shape = (number_of_points, number_of_points,)

    geom = Geometry()

    # Set global information:
    geom.p_direction_0 = np.array([0.0, 0.0, 1.0])
    geom.j_direction_0 = np.array([1.0, 0.0, 0.0])
    geom.k_direction_0 = np.array([0.0, 1.0, 0.0])
    geom.detector_direction_origin = np.array([1.0, 0.0, 0.0])
    geom.detector_direction_positive_90 = np.array([0.0, 1.0, 0.0])
    geom.projection_shape = np.array((number_of_points, 1)).astype(int)
    geom.volume_shape = np.array((tomo_shape[0], 1, tomo_shape[1])).astype(int)
    geom.detector_angles = np.array(azim_angles) * np.pi / 180
    geom.full_circle_covered = True
    geom.full_circle_covered = True

    for ii, rotangle in enumerate(rot_angles):

        R_mat = Ry(rotangle*np.pi/180)
        geom_tp = GeometryTuple(rotation=R_mat,
                                j_offset=offcen_length,
                                k_offset=0.0,)
        geom.append(geom_tp)
    return geom
