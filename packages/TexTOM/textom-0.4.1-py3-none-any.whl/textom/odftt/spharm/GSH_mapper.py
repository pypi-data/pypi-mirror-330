import numpy as np
from mumott.core.wigner_d_utilities import load_d_matrices
from tqdm import tqdm


def GSH_mapper(GSH_coeffs, ell_max, resolution=5.0):
    """ Function used to generate an Euler-angle map of the ODF represented by a set of
    generalized spherical harmonics coefficients.

    Parameters:
    -----------
        GSH_coeffs
            List of GSH coefficients. list should have minium length `ell_max + 1` where the
            `ell`th elemnt is a 2`ell` by 2`ell` array. The coefficients should be in the
            full basis not of the symmetrized coefficients.

            All odd orders are ignored.

        ell_max
            Integer. Maximum GHS order ell to include.

        resolution
            Resolution of the Euler-angles map in degrees. The resolution will only be matched if the input
            is a divisor of 180.

    Returns:
    --------
        ODF_map
            3D numpy array containing the ODF values of the map.

        Euler_angles
            3-length tuple containging three 3D arrays with the coordinates of the map points.
    """

    d_matrices = load_d_matrices(ell_max)

    points_on_circle = int(360 / resolution + 1)
    Phi_map = np.linspace(0, 2 * np.pi, points_on_circle)
    points_on_halfcircle = int(180 / resolution + 1)
    Theta_map = np.linspace(0, np.pi, points_on_halfcircle)
    Psi_map = np.linspace(0, 2 * np.pi, points_on_circle)

    ODF_map = np.zeros((points_on_circle, points_on_halfcircle, points_on_circle))

    for ell in tqdm(range(0, ell_max + 1, 2)):

        GSH_coeffs_this_ell = GSH_coeffs[ell]

        for ii, Phi in enumerate(Phi_map):
            for jj, Theta in enumerate(Theta_map):

                mphi = (np.arange(-ell, ell+1) * Phi)[np.newaxis, :]
                mtheta = (np.arange(-ell, ell+1) * Theta)[np.newaxis, :]

                # Compute D matrix at (Phi, Theta, 0)
                D = np.eye(2*ell + 1)
                D = D[::1, :] * np.cos(mphi) - D[:, ::-1] * np.sin(mphi)  # Rotate Phi about Z
                D = D @ d_matrices[ell].T  # Rotate 90° about y
                D = D[::1, :] * np.cos(mtheta) - D[:, ::-1] * np.sin(mtheta)  # Rotate Theta about Z
                D = D @ d_matrices[ell]  # Rotate -90° about y

                for kk, Psi in enumerate(Psi_map):

                    mpsi = (np.arange(-ell, ell+1) * Psi)[np.newaxis, :]
                    D_psi = D[::1, :] * np.cos(mpsi) - D[:, ::-1] * np.sin(mpsi)
                    ODF_map[ii, jj, kk] += np.sum(GSH_coeffs_this_ell * D_psi)

    return ODF_map, (Phi_map[np.newaxis, np.newaxis, :],
                     Theta_map[np.newaxis, :, np.newaxis],
                     Psi_map[:, np.newaxis, np.newaxis])
