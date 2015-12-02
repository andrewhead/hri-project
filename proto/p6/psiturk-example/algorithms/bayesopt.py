#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import numpy as np
import scipy.stats
from scipy.optimize import minimize
from functools import partial


logging.basicConfig(level=logging.INFO, format="%(message)s")


N = scipy.stats.norm()


def acquire(x, fmap, Cmap, bounds, kernelfunc, extrabounds=lambda p: True):
    '''
    bounds: a numpy array of constraints on each dimension, of the form:
        [
            [lower_bound, upper_bound] # dimension 1,
            [lower_bound, upper_bound] # dimension 2,
            ...
            [lower_bound, upper_bound] # dimension k,
        ]
    extrabounds: an optional function for determining whether a point falls within bounds,
        using more complex rules than a range of numbers.  The extrabounds function
        should return True if a point is within bounds, and False if the point is outside of it.
    '''

    def cost_func(xnew, bounds, extrabounds):
        # Compute the expected value and variance
        f_exp = predict_f(x, fmap, xnew, kernelfunc)
        sigma_exp = predict_sigma(x, fmap, Cmap, xnew, kernelfunc)
        if sigma_exp == 0.0:
            return 0.0

        # If this point falls outside of bounds, give it a low score
        BOUNDS_COST = 10.0
        for dimi in range(bounds.shape[0]):
            if xnew[dimi] < bounds[dimi][0] or xnew[dimi] > bounds[dimi][1]:
                return BOUNDS_COST
        if not extrabounds(xnew):
            return BOUNDS_COST

        # Compute the expected improvement at this point
        dist = f_exp - np.max(fmap)
        z = dist / sigma_exp
        ei = dist * N.cdf(z) + sigma_exp * N.pdf(z)
        return -ei

    avgs = np.average(bounds, axis=1)
    res = minimize(cost_func, avgs, args=(bounds, extrabounds,), method='powell')
    xnew = res.x
    if xnew.shape == ():
        xnew = np.array([xnew])
    return xnew


def predict_f(x, fmap, xnew, kernelfunc):
    k = kernel_vector(kernelfunc, x, xnew)
    K = kernel_matrix(kernelfunc, x)
    Kinv = np.linalg.inv(K)
    kernel_product = k.T.dot(Kinv)
    f = kernel_product.dot(fmap)
    f_elem = f[0][0]
    return f_elem


def predict_sigma(x, fmap, Cmap, xnew, kernelfunc):
    K = kernel_matrix(kernelfunc, x)
    k = kernel_vector(kernelfunc, x, xnew)
    knew = kernelfunc(xnew, xnew)
    # Here, we take a cue from Eric Brochu's source:
    # https://github.com/misterwindupbird/IBO/blob/master/ego/gaussianprocess/__init__.py
    # If C cannot be inverted, then add a "regularizer delta"---I
    try:
        Cinv = np.linalg.inv(Cmap)
        # If the entries are near infinite in the matrix, it was probably singular
        if np.sum(np.abs(Cinv)) > 1e15:
            raise np.linalg.LinAlgError
    except np.linalg.LinAlgError:
        Cinv = np.linalg.inv(Cmap + np.eye(len(Cmap)))
    M = np.linalg.inv(K + Cinv)
    sigma = knew - k.T.dot(M).dot(k)
    sigma_elem = sigma[0][0]
    return sigma_elem


def newton_rhapson(x, f0, comparisons, kernelfunc, Hfunc, gfunc, sigma, maxiter=100):
    f = f0
    i = 0
    while i < maxiter:
        H = Hfunc(kernelfunc, x, f, comparisons, sigma)
        Hinv = np.linalg.inv(H)
        g = gfunc(kernelfunc, x, f, comparisons, sigma)
        step = Hinv.dot(g)
        f = f - step
        i += 1
    Cmap = compute_C(f, comparisons, sigma)
    return f, Cmap


c_products = {}


def c_pdf_cdf_term(z):
    if z not in c_products:
        # The product in the paper is a typo.  This is the right way.
        # See also Eric's implementation at
        # https://github.com/misterwindupbird/IBO/blob/master/ego/gaussianprocess/__init__.py
        phi = N.pdf(z)
        Phi = N.cdf(z)
        if np.isclose(Phi, 0.0):
            c_products[z] = 0.0
        else:
            c_products[z] = (np.power(phi, 2) / np.power(Phi, 2)) + (phi * z / Phi)
    return c_products[z]


z_cached = {}


def compute_z(fr, fc, sigma):
    if (fr, fc, sigma) not in z_cached:
        z_cached[(fr, fc, sigma)] = (fr - fc) / (np.sqrt(2.0) * sigma)
    return z_cached[(fr, fc, sigma)]


def h(comparison, xi):
    r, c = comparison
    return \
        0.0 if xi == r and xi == c else \
        1.0 if xi == r else \
        -1.0 if xi == c else \
        0.0


cdfs = {}
divisions = {}


def b_summand(f, j, comparison, sigma):
    ri, ci = comparison
    fr = f[ri][0]
    fc = f[ci][0]
    z = compute_z(fr, fc, sigma)
    hi = h(comparison, j)
    if z not in cdfs:
        cdfs[z] = N.cdf(z)
    if np.isclose(cdfs[z], 0.0):
        return 0.0
    if z not in divisions:
        divisions[z] = N.pdf(z) / N.cdf(z)
    summand = divisions[z] * hi
    return summand


def b_j(f, j, comparisons, sigma):
    sum_ = 0
    num_comp = comparisons.shape[0]
    for ci in range(num_comp):
        comp = comparisons[ci]
        summand = b_summand(f, j, comp, sigma)
        sum_ += summand
    b = sum_ / (np.sqrt(2) * sigma)
    return b


def compute_b(f, comparisons, sigma):
    # We assume we have the same number of 'f' as we do of 'x'
    b = []
    for fi in range(len(f)):
        b_row = [b_j(f, fi, comparisons, sigma)]
        b.append(b_row)
    return np.array(b)


def compute_g(kernelfunc, x, f, comparisons, sigma):
    K = kernel_matrix(kernelfunc, x)
    Kinv = np.linalg.inv(K)
    b = compute_b(f, comparisons, sigma)
    g = (-1 * Kinv.dot(f)) + b
    return g


def c_summand(f, m, n, comparison, sigma):
    '''
    Params:
    f: vector of evaluations for all points x
    m: index of one point
    n: index of another point
    comparison: two indices, each for one of a pair of points
    sigma: standard deviation of the noise
    '''
    ri, ci = comparison
    fr = f[ri][0]
    fc = f[ci][0]
    z = compute_z(fr, fc, sigma)
    cdf_pdf_term = c_pdf_cdf_term(z)
    hm = h(comparison, m)
    hn = h(comparison, n)
    return hm * hn * cdf_pdf_term


def c_m_n(f, m, n, comparisons, sigma, memo={}):
    sum_ = 0
    num_comp = comparisons.shape[0]
    for ci in range(num_comp):
        comp = comparisons[ci]
        compr, compc = comp.tolist()
        if (m, n, compr, compc) not in memo:
            summand = c_summand(f, m, n, comp, sigma)
            memo[(m, n, compr, compc)] = summand
        else:
            summand = memo[(m, n, compr, compc)]
        sum_ += summand
    c = sum_ / (2 * sigma * sigma)
    return c


def compute_C(f, comparisons, sigma):
    # We assume we have the same number of 'f' as we do of 'x'
    C = []
    memo = {}
    for fi in range(len(f)):
        c_row = []
        for fj in range(len(f)):
            if (fi, fj) not in memo:
                c_entry = c_m_n(f, fi, fj, comparisons, sigma, memo)
                memo[(fi, fj)] = c_entry
                memo[(fj, fi)] = c_entry
            else:
                c_entry = memo[(fi, fj)]
            c_row.append(c_entry)
        C.append(c_row)
    C_np = np.array(C)
    return C_np


def compute_H(kernelfunc, x, f, comparisons, sigma):
    K = kernel_matrix(kernelfunc, x)
    Kinv = np.linalg.inv(K)
    C = compute_C(f, comparisons, sigma)
    H = -Kinv + C
    return H


def get_distinct_x(comparisons):
    xlist = []
    in_list = lambda l, e: len(filter(lambda x: np.allclose(x, e), l)) > 0
    for r, c in comparisons:
        if not in_list(xlist, r):
            xlist.append(r)
        if not in_list(xlist, c):
            xlist.append(c)
    return np.array(xlist)


def get_comparison_indices(x, comparisons):
    indices = []
    row_count = comparisons.shape[0]
    for rowi in range(row_count):
        r, c = comparisons[rowi]
        ri = -1
        ci = -1
        for xi, xe in enumerate(x):
            if np.allclose(r, xe):
                ri = xi
            if np.allclose(c, xe):
                ci = xi
        indices.append([ri, ci])
    return np.array(indices)


def default_kernel(x1, x2, a=-.5):
    diff = x1 - x2
    return np.exp(a * diff.dot(diff))


def kernel_vector(kernelfunc, x, xnew):
    klist = []
    for xe in x:
        klist += [[kernelfunc(xe, xnew)]]
    return np.array(klist)


def kernel_matrix(kernelfunc, x):
    K = []
    for xe1 in x:
        row = []
        for xe2 in x:
            row.append(kernelfunc(xe1, xe2))
        K.append(row)
    return np.array(K)


if __name__ == '__main__':

    sigma = 2.0
    f = np.array([[0.0]])
    x = np.array([
        [0.5, 0.5],
    ])
    comparisons = np.array([])
    bounds = np.array([
        [0.0, 2.0],
        [0.0, 2.0],
    ])
    xnew = np.array([0.0, 0.5])
    kernel = partial(default_kernel, a=-10)

    def _aappend(np_array, element):
        l = np_array.tolist()
        l.append(element)
        return np.array(l)

    while True:

        xnew_i = len(f)
        best_f_i = np.argmax(f)
        xbest = x[best_f_i]

        print "Is", xnew, "better than", xbest, "? (y/n)",
        answer = raw_input()

        comp = [xnew_i, best_f_i] if answer == 'y' else [best_f_i, xnew_i]
        comparisons = _aappend(comparisons, comp)
        f = _aappend(f, [0.0])
        x = _aappend(x, xnew)

        fmap, Cmap = newton_rhapson(
            x, f, comparisons, kernel,
            compute_H, compute_g, sigma, maxiter=10)
        xnew = acquire(x, fmap, Cmap, bounds, kernel)
        f = fmap
        print "x:"
        print x
        print "comparisons"
        print comparisons
        print "f:"
        print f
