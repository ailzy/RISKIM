"""
Data Preprocessing Scaling
"""

import math
import numpy as np
from numpy.random import randint

__all__ = ['standardize_x', 'zeromean_y', 'shuffle']

def scale_train_x(x):
    dim_i_range, dim_j_range = x.shape
    norm_vec, mean_vec = [0] * dim_j_range, [0] * dim_j_range
    x_scaled = x.copy()

    for i in range(dim_i_range):
        for j in range(dim_j_range):
            mean_vec[j] += x_scaled[i][j]

    for j in range(dim_j_range):
        mean_vec[j] /= dim_i_range

    for i in range(dim_i_range):
        for j in range(dim_j_range):
            x_scaled[i][j] -= mean_vec[j]

    for i in range(dim_i_range):
        for j in range(dim_j_range):
            norm_vec[j] += x_scaled[i][j] * x_scaled[i][j]

    for j in range(dim_j_range):
        norm_vec[j] = math.sqrt(norm_vec[j])

    for i in range(dim_i_range):
        for j in range(dim_j_range):
            x_scaled[i][j] /= (norm_vec[j] + 1e-10)

    return x_scaled, norm_vec, mean_vec

def scale_test_x(x, norm_vec, mean_vec):
    dim_i_range, dim_j_range = x.shape
    assert (len(mean_vec) == len(norm_vec) == dim_j_range)
    x_scaled = x.copy()

    for i in range(dim_i_range):
        for j in range(dim_j_range):
            x_scaled[i][j] -= mean_vec[j]
            x_scaled[i][j] /= (norm_vec[j] + 1e-10)

    return x_scaled

def standardize_x(x_train, x_test):
    """
    standardizing train and test instances
    :param x_train:
    :param x_test:
    :return:
    """
    x_train_plus, norm_vec, mean_vec = scale_train_x(x_train)
    x_test_plus = scale_test_x(x_test, norm_vec, mean_vec)
    return x_train_plus, x_test_plus, norm_vec, mean_vec


def zeromean_y(y_train):
    """
    let Y_train centralized at zero
    :param y_train:
    :return:
    """
    lnn = len(y_train)
    y_mean = sum(y_train) / lnn
    for i in range(lnn):
        y_train[i] -= y_mean
    return np.array(y_train), y_mean


def shuffle(x, y):
    """
    a shuffle for making samples disorder
    :param x: Instances Matrix
    :param y: Target Values Vector
    :return: shuffled Instance-Target
    """
    x_copy, y_copy = x.copy(), y.copy()
    dim_i_range, dim_j_range = x.shape
    for i in range(dim_i_range):
        idx = randint(0, dim_i_range - i)
        x_copy[idx + i], x_copy[i] = x_copy[i].copy(), x_copy[idx + i].copy()
        y_copy[idx + i], y_copy[i] = y_copy[i].copy(), y_copy[idx + i].copy()
    return x_copy, y_copy
