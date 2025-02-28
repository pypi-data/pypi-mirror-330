from scipy.special import lpmn, factorial
import numpy as np


def spharm_values_single_ell_unstructured_coords(ell, theta, phi):
    """ Compute all spherical harmonics of a given order ell function on a unstructured
    set of points parametrized by two lists of polar coordinates.

    Parameters:
    -----------
    ell
        Int order of spherical harmonics to compute.
    theta
        1D `np.array` of length `N` containing the polar cooridnates of the points to compute.
    phi
        1D `np.array` of length `N` containing the azimuthal cooridnates of the points to compute.

    Returns:
    --------
    output
        `N` by `2*ell + 1` array containing the computed spherical harmonics values.
    """
    # calculate associated legendre function values
    z_array = np.cos(theta)
    legendre_values = np.zeros([len(theta), ell+1, ell+1])
    for iz, z in enumerate(z_array):
        legendre_values[iz, :, :], _ = lpmn(ell, ell, z)

    # Build array of phi- cos/sine values (could be done with fft)
    m_list = np.arange(-ell, ell+1)
    cos_sin_array = np.zeros((len(theta), ell*2+1))
    mphi = np.einsum('i,j->ij', phi, np.abs(m_list))
    cos_sin_array[:, :ell] = np.sin(mphi[:, :ell])
    cos_sin_array[:, ell:] = np.cos(mphi[:, ell:])

    # Initialize output
    output = np.zeros((len(theta), ell*2 + 1))
    # Loop over orders
    m = np.arange(-ell, ell+1)
    normalization = np.sqrt(2) * np.sqrt((2*ell + 1)*factorial(ell-np.abs(m))
                                         / factorial(ell + np.abs(m)))*(-1)**np.abs(m)
    normalization[ell] = normalization[ell] / np.sqrt(2)
    legendre_list = np.concatenate((np.flip(legendre_values[:, 1:ell+1, ell], axis=1),
                                    legendre_values[:, :ell+1, ell]), axis=1)
    output += np.einsum('tm,tm,m ->tm', legendre_list, cos_sin_array, normalization)

    return output


def map_single_l(ell, coeffs, theta, phi, output=None):
    """ Compute a map of spherical harmonics parametrized by the input coefficients at a fixed
    order `ell` on a regular latitude-longitude map at the unput prid points.

    Parameters:
    -----------
    ell
        Int order of spherical harmonics to compute.
    coeffs
        1D numpy array of length `2*ell + 1` containing the spherical harmonics coefficients
        of the function to be mapped.
    theta
        1D `np.array` of length `N` containing the polar cooridnates of the points to compute.
    phi
        1D `np.array` of length `M` containing the azimuthal cooridnates of the points to compute.
    output (optional)
        `N` by `M` numpy array. If given, the map is added to this array and this array is returned
        Otherwise a new array is created.

    Returns:
    --------
    output
        `N` by `M` array containing the computed map.
    """
    # For this one, theta and phi are 1D arrays, and the returnes values correspond to a meshgrid
    n_theta = len(theta)
    n_phi = len(phi)

    # calculate associated legendre function values
    max_l = ell
    z_array = np.cos(theta)
    legendre_values = np.zeros([n_theta, max_l+1, max_l+1])
    for iz, z in enumerate(z_array):
        legendre_values[iz, :, :], _ = lpmn(max_l, max_l, z)

    # Build array of phi- cos/sine values (could be done with fft)
    m_list = np.arange(-max_l, max_l+1)
    cos_sin_array = np.zeros((n_phi, max_l*2+1))
    mphi = np.einsum('i,j->ij', phi, np.abs(m_list))
    cos_sin_array[:, :max_l] = np.sin(mphi[:, :max_l])
    cos_sin_array[:, max_l:] = np.cos(mphi[:, max_l:])

    # Initialize output
    if output is None:
        output = np.zeros((n_theta, n_phi))
    # Loop over orders

    m = np.arange(-ell, ell+1)
    normalization = np.sqrt(2) * np.sqrt((2*ell + 1) * factorial(ell-np.abs(m))
                                         / factorial(ell+np.abs(m)))*(-1)**np.abs(m)
    normalization[ell] = normalization[ell] / np.sqrt(2)
    legendre_list = np.concatenate((np.flip(legendre_values[:, 1:ell+1, ell], axis=1),
                                    legendre_values[:, :ell+1, ell]), axis=1)
    output += np.einsum('tm,pm,m,m ->tp', legendre_list, cos_sin_array, coeffs, normalization)

    return output


def map_from_spharm_coefficients(max_ell, coeffs, theta, phi):
    """ Compute a map of spherical harmonics parametrized by the input coefficients up to
    a maximum order ell_max.

    Parameters:
    -----------
    max_ell
        Int. Maximum order of spherical harmonics to compute.
    coeffs
        1D numpy array of length `(ell + 1)*(ell + 1)//2` containing the spherical harmonics coefficients
        of the function to be mapped in `mumott` format.
    theta
        1D `np.array` of length `N` containing the polar cooridnates of the points to compute.
    phi
        1D `np.array` of length `M` containing the azimuthal cooridnates of the points to compute.

    Returns:
    --------
    output
        `N` by `M` array containing the computed map.
    """
    n_theta = len(theta)
    n_phi = len(phi)
    output = np.zeros((n_theta, n_phi))

    for ell in range(0, max_ell+1, 2):
        if ell == 0:
            slc = slice(0, 1)
        else:
            slc = slice(ell*(ell - 1)//2, (ell + 1)*(ell + 2)//2)

        map_single_l(ell, coeffs[slc], theta, phi, output=output)

    return output
