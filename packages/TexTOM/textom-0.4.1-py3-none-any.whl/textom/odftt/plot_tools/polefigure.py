import numpy as np


def plot_cubic_asym_outline(ax, color='k'):

    # Plot an outline of the asymmetric zone.
    ax.plot([0, 0], [0, np.arctan(45*np.pi/360)], color=color, linewidth=1.0)
    ax.plot([45*np.pi/180, 45*np.pi/180], [0, np.arctan(np.arccos(1/np.sqrt(3))/2)],
            color=color, linewidth=1.0)
    d1 = np.array([1, 0, 1])
    d2 = np.array([1, 1, 1])

    theta_list = []
    phi_list = []
    for ii in range(200):
        vec = (1 - ii/199)*d1 + ii/199*d2
        vec = vec / np.linalg.norm(vec)
        theta_list.append(np.arctan(np.arccos(vec[2])/2))
        phi_list.append(np.arctan2(vec[1], vec[0]))
    ax.plot(phi_list, theta_list, color=color, linewidth=1.0)

    # Label directions
    ax.text(2.5/2*np.pi, 0.05, '(100)', color=color)
    ax.text(-0.03*np.pi, 0.35, '(110)', color=color)
    ax.text(np.pi/4, 0.45, '(111)', color=color)
