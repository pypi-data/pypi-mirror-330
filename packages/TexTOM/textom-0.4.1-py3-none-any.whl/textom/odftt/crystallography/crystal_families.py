import numpy as np
"""This file contains a number of basic functions to generate lattice matrices and
 reciprocal lattice matrices for the seven lattice systems (if I have finished it!).
 The main use of these functions is to generate the reciprocal lattice matrix, B
 which is used to transform Miller index triplets to vectors in the lattice-coordinate
 system.
    h = B @ np.array([h, k, l])
 """
# TODO: Triclinic, Monoclinic, Rhombohedral, Tetragonal
# *Note to future developer:*
# Be careful when implementing monoclinic and rhobohedral.
# Typically the twofold axis for monoclinic is
# chosen to be 'b', but I have written the cyclic group with 'z'.
# For rhombohedral the 3-fold axis will not be aligned with 'z'
# when the lattice is written in upper-triagonal form.
#
# This should be remedied by taking the input in the conventional
# a, b, c, alpha, beta, gamma format but outputting the matrices
# in the z-axis orientation.
#
# This is very likely to confuse users though.


def cubic(a=1):

    A = np.array([[a, 0, 0],
                  [0, a, 0],
                  [0, 0, a],
                  ]).T
    return A, reciprocal_lattice(A)


def orthohombic(a=1, b=2, c=3):

    A = np.array([[a, 0, 0],
                  [0, b, 0],
                  [0, 0, c],
                  ]).T
    return A, reciprocal_lattice(A)


def hexagonal(a=1, c=1.633):

    A = np.array([[a, 0, 0],
                  [-0.5*a, np.sqrt(3)/2 * a, 0],
                  [0, 0, c],
                  ]).T
    return A, reciprocal_lattice(A)


def reciprocal_lattice(A):
    return 2*np.pi*np.linalg.inv(A).T
