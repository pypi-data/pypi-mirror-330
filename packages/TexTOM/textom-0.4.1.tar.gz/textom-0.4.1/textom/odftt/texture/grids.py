import numpy as np
from scipy.spatial.transform import Rotation as R
from . import point_groups


def hopf_for_cubic(divisions_of_edge):
    """ Create a grid of orientations that is compatible with the octahedral symmetry goup 432.
    The grid is based on a uniformly sampling one face of teh cube and using the Hopf fibration.
    I couldn't quite get it to work, so in the end I have to trim some orientations outside of
    the asymmetric zone.

    Parameters:
    -----------
    divisions_of_edge
        Integer. Sets the resolution of the grid. The number of grid-points scales roughly
        with this number cubed.
    Returns:
    --------
        grid
            `scipy` rotations object containing the grid orientations.
    """
    # Gnomonic grid of one face of the cube
    halfstep = 1.5 / divisions_of_edge
    halfstep_rad = 0.5 * np.pi/2 / divisions_of_edge
    ang1 = np.linspace(-np.pi/3 + halfstep_rad, np.pi/3 - halfstep_rad, divisions_of_edge)
    ang1, ang2 = np.meshgrid(ang1, ang1)
    x = np.tan(ang1)
    y = np.tan(ang2)
    vectors = np.stack((x.ravel(), y.ravel(), np.ones(x.shape).ravel()), axis=-1)
    vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]

    rotvecs = np.cross(vectors, [0, 0, 1])
    norm = np.arccos(vectors[:, 2])
    rotvecs = rotvecs / np.linalg.norm(rotvecs, axis=-1)[:, np.newaxis] * norm[:, np.newaxis]
    # Exception handling for the identity rotation
    if divisions_of_edge % 2 == 1:
        rotvecs[(divisions_of_edge+1)*((divisions_of_edge-1)//2), :] = [0, 0, 0]
    rotations_somepart = R.from_rotvec(rotvecs)
    # Compose full rotation as a combination of a z-rotation and the min rotation to the grid
    psis = np.linspace(-np.pi/4 + halfstep, np.pi/4 - halfstep, divisions_of_edge)
    # psis = np.zeros(1)
    rotvec_full = np.zeros((divisions_of_edge**3, 3))
    for ii, psi in enumerate(psis):
        # Geometric interpretation of Hopf fibration
        Rot_z = R.from_euler('z', psi)
        rotvec_full[(ii*divisions_of_edge**2):((ii+1)*divisions_of_edge**2)]\
            = (rotations_somepart * Rot_z).as_rotvec()
    rotations_full = R.from_rotvec(rotvec_full)

    # Trim away orientations outside the fundamental zone
    good_indexes = np.ones(len(rotations_full), dtype=bool)
    norm_base = rotations_full.magnitude()
    for gsym in point_groups.octahedral:
        norm = (rotations_full*gsym).magnitude()
        good_indexes[norm < norm_base] = False

    return rotations_full[good_indexes]


def random_quarternions(num_of_orientations):
    """ Create a grid of random orientations. Used for testing purposes.
    """
    rng = np.random.default_rng()
    fourvectors = rng.normal(size=(num_of_orientations, 4))
    fourvectors[:, 3] = np.abs(fourvectors[:, 3])
    quarternions = fourvectors / np.linalg.norm(fourvectors, axis=1)[:, np.newaxis]
    rotations = R.from_quat(quarternions)
    return rotations


def uniform_euler(div_of_2pi):
    """ Make a grid by uniformly sampling euler-angle space. Not very useful!
    """
    Psi = np.linspace(0, 2*np.pi, div_of_2pi, endpoint=False)
    Theta = np.linspace(0, np.pi, div_of_2pi//2)
    Phi = np.linspace(0, 2*np.pi, div_of_2pi, endpoint=False)
    Psi, Theta, Phi = np.meshgrid(Psi, Theta, Phi)
    rotations = R.from_euler('zyz', np.stack((Psi.ravel(), Theta.ravel(), Phi.ravel(),)).T)
    return rotations


def hopf_grid(divisions_of_pi, point_group):
    """ Create a grid of orientations map out all of SO(3) and crop it to the fundamental
    zone of the input point group.
    The grid is based on a latitude longitude map of the unit half sphere as well and the
    Hopf fibration.
    The grid is cropped uding floating-point comparisons, so the output is system-dependent!
    Don't rely on this function returning the same array on different machines. Always save
    a copy of the grid along with you reconstruction.

    Parameters:
    -----------
    divisions_of_pi
        Integer. Sets the resolution of the grid. The number of grid-points scales roughly
        with this number cubed.
    point_group
        List of rotations defining the point group of which to map the funcamental zone.
    Returns:
    --------
        grid
            `scipy` rotations object containing the grid orientations.
    """
    # Make a grid of points on the unit-half-sphere
    # Number of points on the half-sphere
    N = 2*divisions_of_pi**2
    # Area pr point
    A = 4*np.pi
    a = A/N
    # Approximate distance between points
    d = np.sqrt(a)
    # Number of theta-values to include
    theta_range = np.pi
    M_theta = round(theta_range / d)
    d_theta = theta_range / M_theta
    # Stepsize in phi at equator
    d_phi = a / d_theta
    theta_list = []
    phi_list = []
    for m in range(M_theta):
        theta = np.pi - theta_range * (m + 0.5) / M_theta
        M_phi = round(2*np.pi*np.sin(theta)/d_phi)
        if M_phi == 0:
            M_phi = 1

        for n in range(M_phi):
            phi = 2*np.pi*n/M_phi
            theta_list.append(theta)
            phi_list.append(phi)

    theta = np.array(theta_list)
    phi = np.array(phi_list)
    vectors = np.stack((np.sin(theta)*np.cos(phi),
                        np.sin(theta)*np.sin(phi),
                        np.cos(theta),), axis=-1)

    # Find smallest rotation that carries z-axis onto the grid
    rotvecs = np.cross(vectors, [0, 0, 1])
    norm = np.arccos(vectors[:, 2])
    rotvecs = rotvecs / np.linalg.norm(rotvecs, axis=-1)[:, np.newaxis] * norm[:, np.newaxis]
    rotations_somepart = R.from_rotvec(rotvecs)
    # Compose full rotation as a combination of a z-rotation and the min rotation to the grid
    psis = np.linspace(-np.pi + np.pi/2/divisions_of_pi, np.pi + np.pi/2/divisions_of_pi, 2
                       * divisions_of_pi, endpoint=False)
    rotvec_full = np.zeros((2*divisions_of_pi*len(theta), 3))
    for ii, psi in enumerate(psis):
        # Geometric interpretation of Hopf fibration
        Rot_z = R.from_euler('z', psi)
        rotvec_full[(ii*len(theta)):((ii+1)*len(theta))]\
            = (rotations_somepart * Rot_z).as_rotvec()

    rotations_full = R.from_rotvec(rotvec_full)
    # Trim away orientations outside the fundamental zone
    good_indexes = np.ones(len(rotations_full), dtype=bool)
    norm_base = rotations_full.magnitude()
    for gsym in point_group[1:]:
        norm = (rotations_full*gsym).magnitude()
        good_indexes[norm <= norm_base] = False

    return rotations_full[good_indexes]
