import numpy as np
from odftt.plot_tools.point_groups import plot_asym_zone_outline
import matplotlib as mpl


def plot_orientation_coeffs(voxel_coeffs, orientations, ax,
                            plot_relative_threshold=0, point_group_string=None, size=10):

    max_coeff = np.max(voxel_coeffs)

    rotvec = orientations.as_rotvec()
    nonzero_indexes = np.arange(len(orientations))[voxel_coeffs > plot_relative_threshold*max_coeff]

    for jj in nonzero_indexes:
        ax.plot(rotvec[jj, 0], rotvec[jj, 1], rotvec[jj, 2], '.',
                markersize=size*np.sqrt(voxel_coeffs[jj] / max_coeff),
                color=mpl.colormaps['viridis'](voxel_coeffs[jj] / max_coeff))

    if point_group_string is not None:
        plot_asym_zone_outline(ax, point_group_string)
