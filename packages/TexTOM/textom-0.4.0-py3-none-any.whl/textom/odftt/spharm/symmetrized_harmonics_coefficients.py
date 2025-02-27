from mumott.core.wigner_d_utilities import load_d_matrices
import numpy as np


def find_cubic_harmonics(ell, d_matrices):
    """ Calculate the cubic-symmetric (432) surface harmonics at a single
    order ell. Found by solving the eigen-problem of the R_y(90°) D-matrix
    expressed in the egenvalue +1 sub-space of the (much simpler) R_z(90°)
    D-matrix.

    Parameters:
    -----------

    ell (int)
        Primary quantum number.
    d_matrices (list(np.array))
        List of precalculated R_y(90°) D-matrixes.

    Returns:
        List of dictionaries containing the coefficients of the symmetric modes.
        List will be empty if no modes are found at this order (ell = 2 and ell = 3).
    """

    d = d_matrices[ell]

    # 90deg z part
    p = ell//4
    m_values = np.arange(0, 4*p+1, 4)
    indexes = m_values + ell
    d_sym = d[indexes, :]
    d_sym = d_sym[:, indexes]

    # Solve p by p eigenvalue problem
    eigvals, eigvecs = np.linalg.eig(d_sym)
    eigvecs_unitary_subspace = []
    cubic_harmonics_coeffs = []
    for ii, val in enumerate(eigvals):

        if np.isclose(val, 1):
            eigvecs_unitary_subspace.append(eigvecs[:, ii])
            # coeffs = np.zeros(2*ell + 1)
            # coeffs[m_values + ell] = eigvecs[:, ii]
            # dd = {'ell': ell, 'coeffs': coeffs}
            # cubic_harmonics_coeffs.append(dd)

    if len(eigvecs_unitary_subspace) == 0:
        return cubic_harmonics_coeffs

    eigvecs_unitary_subspace = np.stack(eigvecs_unitary_subspace, axis=0)

    # If degenerate, do gram-schmidt
    if eigvecs_unitary_subspace.shape[0] > 1:
        _, eigvecs_unitary_subspace = np.linalg.qr(eigvecs_unitary_subspace, mode='complete')
        eigvecs_unitary_subspace = np.flipud(eigvecs_unitary_subspace)

        # Orthorgonalize the modes
        N = eigvecs_unitary_subspace.shape[0]
        for ii in range(0, N-1):
            a = eigvecs_unitary_subspace[ii]
            for jj in range(ii+1, N):
                b = eigvecs_unitary_subspace[jj]
                b_projon_a = (a @ b) * a / np.linalg.norm(a)**2
                eigvecs_unitary_subspace[jj] -= b_projon_a
        eigvecs_unitary_subspace = eigvecs_unitary_subspace\
            / np.linalg.norm(eigvecs_unitary_subspace, axis=1)[:, np.newaxis]

    # wrap up into nice structure
    for eigvec in eigvecs_unitary_subspace:
        coeffs = np.zeros(2*ell + 1)
        first_nonzero_element = eigvec[np.abs(eigvec) > 0.0][0]
        coeffs[m_values + ell] = np.real(eigvec) / np.sign(first_nonzero_element)
        dd = {'ell': ell, 'coeffs': coeffs}
        cubic_harmonics_coeffs.append(dd)

    return cubic_harmonics_coeffs


def make_cube_sph_modes(ell_max):
    """ Calculate the cubic-symmetric (432) surface harmonics at all orders up to `ell_max`.

    Parameters:
    -----------
    ell_max (int)
        Primary quantum number.

    Returns:
        List of dictionaries containing the coefficients of the symmetric modes.
        List will be empty if no modes are found at this order (ell = 2 and ell = 3).
    """
    d_matrices = load_d_matrices(ell_max)
    modes = []

    for ell in range(0, ell_max+1, 2):
        m = find_cubic_harmonics(ell, d_matrices)
        for mode in m:
            modes.append(mode)
    return modes


def make_hexagonal_sph_modes(ell_max):
    """ Calculate the hexagonal-symmetric (62) surface harmonics at all orders up to `ell_max`.
    These are just all the m>0, m%6 = 0 modes, but they have to be wrapped up into a specific
    format.

    Parameters:
    -----------
    ell_max (int)
        Primary quantum number.

    Returns:
        List of dictionaries containing the coefficients of the symmetric modes.
        List will be empty if no modes are found at this order (ell = 2 and ell = 3).
    """
    modes = []

    for ell in range(0, ell_max+1, 2):
        for emm in range(0, ell+1, 6):
            coeffs = np.zeros(2 * ell + 1)
            coeffs[ell + emm] = 1
            modes.append({'ell': ell, 'coeffs': coeffs})
    return modes
