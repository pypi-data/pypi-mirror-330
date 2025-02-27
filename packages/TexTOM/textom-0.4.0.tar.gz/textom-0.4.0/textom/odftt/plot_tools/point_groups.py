from odftt.texture.point_groups import cyclic_4
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp
import numpy as np
""" Plotting routines to draw outlines of the asummetric zones of the various point groups in
Rodriguez vector space.
"""

# TODO: Probably don't need all, but at least orthogonal would be nice.


def plot_asym_zone_outline(ax, point_group_string):

    if point_group_string == 'cubic':
        plot_cubic_asym_zone_outline(ax)
        set_rotvec_ax(ax, np.pi/4)
    elif point_group_string == 'hexagonal':
        plot_hexagonal_asym_zone_outline(ax)
        set_rotvec_ax(ax, np.pi/2)
    elif point_group_string == 'orthogonal':
        plot_ortho_asym_zone_outline(ax)
        set_rotvec_ax(ax, np.pi/2)
    else:
        print(f"Point group '{point_group_string}' nor recognized.")


def set_rotvec_ax(ax, orientation_range=np.pi):

    ax.set_xticks([-np.pi/2, -np.pi/4, 0, np.pi/4, np.pi/2],
                  [r'$-\pi/2$', r'$-\pi/4$', r'$0$', r'$\pi/4$', r'$\pi/2$'])
    ax.set_yticks([-np.pi/2, -np.pi/4, 0, np.pi/4, np.pi/2],
                  [r'$-\pi/2$', r'$-\pi/4$', r'$0$', r'$\pi/4$', r'$\pi/2$'])
    ax.set_zticks([-np.pi/2, -np.pi/4, 0, np.pi/4, np.pi/2],
                  [r'$-\pi/2$', r'$-\pi/4$', r'$0$', r'$\pi/4$', r'$\pi/2$'])
    ax.set_xlim([-orientation_range*1.1, orientation_range*1.1])
    ax.set_ylim([-orientation_range*1.1, orientation_range*1.1])
    ax.set_zlim([-orientation_range*1.1, orientation_range*1.1])
    ax.set_aspect('equal')


def plot_slerp_between(ax, vertex_1, vertex_2):
    slerp = Slerp([0, 1], R.from_rotvec([vertex_1, vertex_2]))
    rotvecs = slerp(np.linspace(0, 1, 21)).as_rotvec()
    ax.plot(rotvecs[:, 0], rotvecs[:, 1], rotvecs[:, 2], 'k--')


def plot_cubic_asym_zone_outline(ax):
    """ In reality, the lines should be curves, but for this small a section of orientation-space,
    the difference is not so noticeable.
    """

    v = np.array([1+np.sqrt(2), 1+np.sqrt(2), 1])
    # I don't have an analytical expression for this magic constant
    v = v / np.linalg.norm(v) * 62.7994296 * np.pi / 180
    vertex_0 = v

    triangle = np.stack([vertex_0, np.roll(vertex_0, 1), np.roll(vertex_0, 2), np.roll(vertex_0, 3)], axis=0)
    line = [v, np.array([v[0], v[1], -v[2]])]
    line2 = [np.array([v[1], v[2], v[0]]), np.array([v[1], -v[2], v[0]])]

    for rot in cyclic_4:

        rotated_triangle = rot.apply(triangle)
        ax.plot(rotated_triangle[:, 0], rotated_triangle[:, 1], rotated_triangle[:, 2], '--k')
        rotated_triangle = -rotated_triangle
        ax.plot(rotated_triangle[:, 0], rotated_triangle[:, 1], rotated_triangle[:, 2], '--k')

        rotated_line = rot.apply(line)
        ax.plot(rotated_line[:, 0], rotated_line[:, 1], rotated_line[:, 2], '--k')
        rotated_line = rot.apply(line2)
        ax.plot(rotated_line[:, 0], rotated_line[:, 1], rotated_line[:, 2], '--k')
        rotated_line = -rot.apply(line2)
        ax.plot(rotated_line[:, 0], rotated_line[:, 1], rotated_line[:, 2], '--k')


def plot_cubic_asym_zone_outline_misorientations(ax):
    """ In reality, the lines should be curves, but for this small a section of orientation-space,
    the difference is not so noticeable.
    """

    v = np.array([1+np.sqrt(2), 1+np.sqrt(2), 1])
    # I don't have an analytical expression for this magic constant
    v = v / np.linalg.norm(v) * 62.7994296 * np.pi / 180
    origin = [0, 0, 0]
    vertex_0 = np.array([v[0], v[2], v[1]])
    vertex_1 = np.array([1, 1, 1]) / np.sqrt(3) * 60 * np.pi / 180
    vertex_2 = 0.5 * np.array([v[0], v[2], v[1]]) + 0.5 * np.array([v[2], v[1], v[1]])
    vertex_3 = np.array([0, 0, 1]) / np.sqrt(1) * 45 * np.pi / 180
    vertex_4 = np.array([v[0], 0, v[0]])

    for v1, v2 in [(origin, vertex_0), (origin, vertex_1), (vertex_1, vertex_0), (vertex_1, vertex_2),
                   (vertex_3, vertex_2), (origin, vertex_3), (vertex_2, vertex_0), (origin, vertex_4),
                   (vertex_4, vertex_3), (vertex_4, vertex_0)]:
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], '--k', linewidth=0.4)


def plot_hexagonal_asym_zone_outline(ax):
    """ In reality, the lines should be curves, but for this small a section of orientation-space,
    the difference is not so noticeable.
    """
    base_points = base_points = R.from_euler('zyz', [[0, np.pi/2, np.pi/6],
                                                     [-np.pi/6, np.pi/2, np.pi/3],
                                                     [-np.pi/3, np.pi/2, np.pi/6],
                                                     [-np.pi/6, np.pi/2, 0]])
    vert_bar = base_points.as_rotvec()
    for rot in R.from_euler('z', np.arange(12)*np.pi/6):
        vert_bar_here = rot.apply(vert_bar)
        ax.plot(vert_bar_here[:, 0], vert_bar_here[:, 1], vert_bar_here[:, 2], 'k--')


def plot_ortho_asym_zone_outline(ax):
    vertex_1 = np.array([1, 1, 1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_2 = np.array([1, 1, -1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_3 = np.array([1, -1, 1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_4 = np.array([-1, 1, 1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_5 = np.array([1, -1, -1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_6 = np.array([-1, 1, -1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_7 = np.array([-1, -1, 1])/np.sqrt(3) * 120 * np.pi / 180
    vertex_8 = np.array([-1, -1, -1])/np.sqrt(3) * 120 * np.pi / 180

    for v1, v2 in [(vertex_1, vertex_2),
                   (vertex_1, vertex_3),
                   (vertex_1, vertex_4),
                   (vertex_2, vertex_5),
                   (vertex_2, vertex_6),
                   (vertex_3, vertex_5),
                   (vertex_3, vertex_7),
                   (vertex_4, vertex_6),
                   (vertex_4, vertex_7),
                   (vertex_5, vertex_8),
                   (vertex_6, vertex_8),
                   (vertex_7, vertex_8),]:
        plot_slerp_between(ax, v1, v2)
