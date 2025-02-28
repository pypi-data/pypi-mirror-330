from matplotlib.colors import hsv_to_rgb
import numpy as np
""" Various function meant to help creating EBSD-style inverse pole figure maps.
"""


def halfsphere_color(vectors):

    vectors = np.copy(vectors)
    whereflip = vectors[..., 1] < 0
    vectors[whereflip, :] = -vectors[whereflip, :]

    theta = np.arccos(vectors[..., 1])
    phi = np.arctan2(vectors[..., 2], vectors[..., 0])
    hue = ((phi) % (np.pi))/np.pi
    saturation = (np.arctan(theta/2) / np.arctan(np.pi/4))**2
    modifier = -np.sin(phi)*np.sin(2*theta)**2
    modifier = np.sign(modifier) * np.abs(modifier)
    value = np.ones(theta.shape)*0.7 + 0.2*modifier

    hsv = np.stack([hue, saturation, value], axis=-1)
    return hsv_to_rgb(hsv)


def IPF_color(vectors, point_group_string):

    if point_group_string == 'cubic':
        return IPF_color_cubic(vectors)
    elif point_group_string == 'hexagonal':
        return IPF_color_hexagonal(vectors)
    elif point_group_string == 'orthogonal':
        return IPF_color_ortho(vectors)
    else:
        print(f"Point group '{point_group_string}' nor recognized.")


def make_color_legend(ax, point_group_string):

    if point_group_string == 'cubic':
        make_color_legend_cubic(ax)
    elif point_group_string == 'hexagonal':
        make_color_legend_hex(ax)
    elif point_group_string == 'orthogonal':
        make_color_legend_ortho(ax)
    else:
        print(f"Point group '{point_group_string}' nor recognized.")


def cast_vectors_to_fundamental_zone_cubic(vectors):

    vectors = np.copy(vectors)
    vectors = np.clip(vectors, -1, 1)

    # Invert if z negative
    indx = vectors[..., 2] < 0
    vectors[indx, :] = -vectors[indx, :]
    # Rotate around z to bring into first quadrant
    phi = np.arctan2(vectors[..., 1], vectors[..., 0])
    theta = np.arccos(vectors[..., 2])
    phi = phi % (np.pi/2)

    # Mirror in x = y if in second octant
    indx = phi > np.pi/4
    phi[indx] = np.pi/2 - phi[indx]
    vectors = np.stack([
                        np.sin(theta)*np.cos(phi),
                        np.sin(theta)*np.sin(phi),
                        np.cos(theta),], axis=-1
                       )

    # Mirror in x = z if x > z
    indx = vectors[..., 0] > vectors[..., 2]
    tmp = np.array(vectors[indx, 0])
    vectors[indx, 0] = vectors[indx, 2]
    vectors[indx, 2] = tmp
    # Rotate around z to bring into first quadrant
    phi = np.arctan2(vectors[..., 1], vectors[..., 0])
    theta = np.arccos(vectors[..., 2])
    phi = phi % (np.pi/2)

    # Mirror in x = y if in second octant
    indx = phi > np.pi/4
    phi[indx] = np.pi/2 - phi[indx]
    vectors = np.stack([
                        np.sin(theta)*np.cos(phi),
                        np.sin(theta)*np.sin(phi),
                        np.cos(theta),], axis=-1
                       )
    return vectors


def cast_vectors_to_fundamental_zone_ortho(vectors):
    return np.abs(vectors)


def cast_vectors_to_fundamental_zone_hexagonal(vectors):

    vectors = np.copy(vectors)
    where_flip = vectors[..., 2] < 0
    vectors[where_flip, :] = -vectors[where_flip, :]

    theta = np.arccos(vectors[..., 2])
    phi = np.arctan2(vectors[..., 1], vectors[..., 0])
    phi = phi % (np.pi/3)

    where_mirror = phi > np.pi/6
    phi[where_mirror] = np.pi/3 - phi[where_mirror]

    vectors = np.stack([np.sin(theta)*np.cos(phi),
                        np.sin(theta)*np.sin(phi),
                        np.cos(theta),
                        ], axis=-1)

    return vectors


def IPF_color_ortho(vectors):

    barycenter_ortho = np.array([0, 0, 1]) + np.array([0, 1, 0]) + np.array([1, 0, 0])
    barycenter_ortho = barycenter_ortho / np.linalg.norm(barycenter_ortho)
    vectors = cast_vectors_to_fundamental_zone_ortho(vectors)
    dist_to_barycenter = np.arccos(vectors[..., 0]*barycenter_ortho[0]
                                   + vectors[..., 1]*barycenter_ortho[1]
                                   + vectors[..., 2]*barycenter_ortho[2])
    saturation = dist_to_barycenter * 1.5
    saturation = np.clip(saturation, 0, 1)

    angle = np.arctan2(vectors[..., 1] - barycenter_ortho[1],
                       vectors[..., 0] - barycenter_ortho[0])
    hue = (angle/np.pi/2) % 1
    hsv = np.stack([hue,
                    saturation,
                    0.2*saturation + 0.8*np.ones((vectors.shape[0], vectors.shape[1]))], axis=-1)
    return hsv_to_rgb(hsv)


def IPF_color_cubic(vectors):

    barycenter_cubic = np.array([0, 0, 1]) + np.array([1, 0, 1])/np.sqrt(2) + np.array([1, 1, 1])/np.sqrt(3)
    barycenter_cubic = barycenter_cubic / np.linalg.norm(barycenter_cubic)
    vectors = cast_vectors_to_fundamental_zone_cubic(vectors)

    dist_to_barycenter = np.arccos(vectors[..., 0]*barycenter_cubic[0]
                                   + vectors[..., 1]*barycenter_cubic[1]
                                   + vectors[..., 2]*barycenter_cubic[2])
    saturation = dist_to_barycenter * 3
    saturation = np.clip(saturation, 0, 1)
    angle = np.arctan2(vectors[..., 1] - barycenter_cubic[1], vectors[..., 0] - barycenter_cubic[0])
    hue = (angle/np.pi/2 + 0.5) % 1
    hsv = np.stack([hue,
                    saturation,
                    0.2*saturation + 0.8*np.ones((vectors.shape[0], vectors.shape[1]))], axis=-1)
    return hsv_to_rgb(hsv)


def IPF_color_hexagonal(vectors):

    barycenter_ortho = np.array([0, 0, 1]) + np.array([np.sqrt(3), 1, 0])/2 + np.array([1, 0, 0])
    barycenter_ortho = barycenter_ortho / np.linalg.norm(barycenter_ortho)
    vectors = cast_vectors_to_fundamental_zone_hexagonal(vectors)
    vectors[..., 1] = vectors[..., 1]*1
    barycenter_ortho[1] = barycenter_ortho[1]*1
    barycenter_ortho = barycenter_ortho / np.linalg.norm(barycenter_ortho)
    vectors = vectors / np.linalg.norm(vectors, axis=-1)[..., np.newaxis]
    dist_to_barycenter = np.arccos(vectors[..., 0]*barycenter_ortho[0]
                                   + vectors[..., 1]*barycenter_ortho[1]
                                   + vectors[..., 2]*barycenter_ortho[2])
    saturation = dist_to_barycenter * 2.0
    saturation = np.clip(saturation, 0, 1)

    angle = np.arctan2(vectors[..., 1] - barycenter_ortho[1],
                       vectors[..., 0] - barycenter_ortho[0])
    hue = (angle/np.pi/2 + 0.5) % 1
    hsv = np.stack([hue,
                    saturation,
                    0.2*saturation + 0.8*np.ones((vectors.shape[0], vectors.shape[1]))], axis=-1)
    return hsv_to_rgb(hsv)


def make_color_legend_cubic(ax):
    theta_grid = np.linspace(0, np.pi/3, 200, endpoint=True)
    phi_grid = np.linspace(0, np.pi/4, 200, endpoint=True)
    theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')
    coords_vector = np.stack([np.sin(theta_grid)*np.cos(phi_grid),
                              np.sin(theta_grid)*np.sin(phi_grid),
                              np.cos(theta_grid),], axis=-1
                             )

    color_legend = IPF_color_cubic(coords_vector)

    # Crop to asymmetric zone
    color_legend[phi_grid > 45*np.pi/180] = 1
    grid_x = np.cos(phi_grid)*np.sin(theta_grid)
    grid_z = np.cos(theta_grid)
    color_legend[grid_x+0.008 > grid_z] = 1

    ax.pcolormesh(phi_grid, np.arctan(theta_grid/2), color_legend, edgecolors='face', rasterized=True)
    ax.set_yticks([np.arctan(ii*np.pi/8) for ii in range(1, 2)])
    ax.set_yticklabels(['45°'])
    ax.yaxis.label.set_color('w')
    ax.set_xlim(0, 45*np.pi/180)
    ax.set_ylim(0, np.tan(59*np.pi/180/2))
    ax.axis('off')

    # Plot an outline of the asymmetric zone.
    ax.plot([0, 0], [0, np.arctan(45*np.pi/360)], 'k', linewidth=3.0)
    ax.plot([45*np.pi/180, 45*np.pi/180], [0, np.arctan(np.arccos(1/np.sqrt(3))/2)], 'k', linewidth=2.0)
    d1 = np.array([1, 0, 1])
    d2 = np.array([1, 1, 1])

    theta_list = []
    phi_list = []
    for ii in range(200):
        vec = (1 - ii/199)*d1 + ii/199*d2
        vec = vec / np.linalg.norm(vec)
        theta_list.append(np.arctan(np.arccos(vec[2])/2))
        phi_list.append(np.arctan2(vec[1], vec[0]))
    ax.plot(phi_list, theta_list, 'k', linewidth=2.0)

    # Label directions
    ax.text(2.5/2*np.pi, 0.05, '(100)')
    ax.text(-0.03*np.pi, 0.45, '(110)')
    ax.text(np.pi/4+0.1, 0.50, '(111)')

    return 0


def make_color_legend_ortho(ax):
    theta_grid = np.linspace(0, np.pi/2, 600, endpoint=True)
    phi_grid = np.linspace(0, np.pi/2, 600, endpoint=True)
    theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

    coords_vector = np.stack([np.sin(theta_grid)*np.cos(phi_grid),
                              np.sin(theta_grid)*np.sin(phi_grid),
                              np.cos(theta_grid),], axis=-1)

    color_legend = IPF_color_ortho(coords_vector)
    ax.pcolormesh(phi_grid, np.arctan(theta_grid/2), color_legend, edgecolors='face', rasterized=True)
    ax.set_yticks([np.arctan(ii*np.pi/8) for ii in range(3)])
    ax.set_yticklabels(['', '', ''])
    ax.set_xticks([ii*np.pi/4 for ii in range(1, 2)])
    ax.set_xticklabels([])
    ax.yaxis.label.set_color('w')
    ax.set_xlim(0, 90*np.pi/180)
    ax.set_ylim(0, np.arctan(90*np.pi/180/2))

    # Label directions
    ax.text(2.5/2*np.pi, 0.1, '(001)')
    ax.text(1.05*np.pi/2, 0.715, '(010)')
    ax.text(-0.12, 0.6, '(100)')


def make_color_legend_hex(ax):
    theta_grid = np.linspace(0, np.pi/2, 600, endpoint=True)
    phi_grid = np.linspace(0, np.pi/6, 200, endpoint=True)
    theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

    coords_vector = np.stack([np.sin(theta_grid)*np.cos(phi_grid),
                              np.sin(theta_grid)*np.sin(phi_grid),
                              np.cos(theta_grid),], axis=-1)

    color_legend = IPF_color_hexagonal(coords_vector)
    ax.pcolormesh(phi_grid, np.arctan(theta_grid/2), color_legend, edgecolors='face', rasterized=True)
    ax.set_yticks([np.arctan(ii*np.pi/12) for ii in range(4)])
    ax.set_yticklabels(['', '', '', ''])
    ax.set_xticks([ii*np.pi/6 for ii in range(1, 2)])
    ax.set_xticklabels([])
    ax.yaxis.label.set_color('w')
    ax.set_xlim(0, 30*np.pi/180)
    ax.set_ylim(0, np.arctan(90*np.pi/180/2))

    # Label directions
    ax.text(2.5/2*np.pi, 0.25, '[001]\n[0001]')
    ax.text(0.35*np.pi/2, 0.715, '[210]\n[101\U000003050]')  # unicode for the combining overline character
    ax.text(-0.3, 0.6, '[100]\n[21\U000003051\U000003050]')


def make_color_wheel(ax):

    theta_grid = np.linspace(0, np.pi/2, 100, endpoint=True)
    phi_grid = np.linspace(0, 2*np.pi, 600, endpoint=True)
    theta_grid, phi_grid = np.meshgrid(theta_grid, phi_grid, indexing='ij')

    coords_vector = np.stack([np.sin(theta_grid)*np.sin(-phi_grid),
                              np.cos(theta_grid),
                              np.sin(theta_grid)*np.cos(phi_grid),], axis=-1)

    color_legend = halfsphere_color(coords_vector)

    ax.pcolormesh(phi_grid, np.arctan(theta_grid/2), color_legend, edgecolors='face', rasterized=True)
    ax.set_yticks([np.arctan(ii*np.pi/8) for ii in range(3)])
    ax.set_yticklabels(['', '', ''])

    ax.set_xticks([ii*np.pi/4 for ii in range(8)])
    ax.set_xticklabels([])

    ax.yaxis.label.set_color('w')
    # plt.title('IPF color legend')
    ax.set_xlim(0, 360*np.pi/180)
    ax.set_ylim(0, np.arctan(90*np.pi/180/2))
    # plt.axis('off')

    # Label directions
    ax.text(2.98*np.pi/2, 0.785, 'x')
    ax.text(-0.03, 0.7, 'z')
