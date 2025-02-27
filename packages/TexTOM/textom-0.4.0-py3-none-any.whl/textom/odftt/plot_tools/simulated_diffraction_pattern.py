import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_simulated_diffraction_pattern(geometry, twothetas_list, scatt_data=None, ax=None,
                                       cmap=mpl.cm.get_cmap('viridis'), maxdata=None,
                                       mindata=0, bg_color=None):

    if ax is None:
        ax = plt.subplot(1, 1, 1)

    if bg_color is None:
        ax.imshow(np.zeros((2, 2)), extent=(-1, 1, -1, 1))
    else:
        bg = np.zeros((2, 2, 3))
        bg[...] = np.array(bg_color)[np.newaxis, np.newaxis, :]
        ax.imshow(bg, extent=(-1, 1, -1, 1))

    if scatt_data is not None:
        if maxdata is None:
            maxdata = np.max(scatt_data)

    azim_angles = geometry.detector_angles
    azim_step = np.abs(azim_angles[1]-azim_angles[0])

    for azim_index, azim_angle in enumerate(azim_angles):
        azim_start = azim_angle - azim_step/3
        azim_end = azim_angle + azim_step/3
        azim_values = np.linspace(azim_start, azim_end, 7)
        x = np.cos(azim_values)
        y = np.sin(azim_values)

        for hkl_index in range(len(twothetas_list)):
            if scatt_data is not None:
                color = cmap((scatt_data[azim_index, hkl_index] - mindata) / (maxdata-mindata))
                ax.plot(x * np.tan(twothetas_list[hkl_index]), y * np.tan(twothetas_list[hkl_index]),
                        color=color, linewidth=2)

            ax.plot(x[3] * np.tan(twothetas_list[hkl_index]), y[3] * np.tan(twothetas_list[hkl_index]),
                    '-', color=[0.5, 0.5, 0.5], linewidth=1)
