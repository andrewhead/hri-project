# Prototype 4: Steepest Ascent with a Second-Order Approximation

## Overview

### Purpose

Box \&amp; Draper suggest using a first or second-order approximation of a response function and following its gradient to ascend to some maximum.
In their formulation, this was the first step before a factorial experiment would be used to determine an empirical model.
For our study, we'll consider using it as a standalone step to approximate the ideal configuration.

### Summary


## Procedure

### Construction

Interaction looks like this:
1. The system asks for a score from 1 to 5 at each of the corners of the distribution.
2. Based on this, it develops a first second-order approximation of the data
3. Using the first-order terms if they are bigger than the second-order terms or all the terms if the second-order terms are larger, we compute the gradient and the next step from the current point.
4. Repeat steps 2 and 3 until the step size is less than .05 of the size of the space of one of the standardized variables.

To generate the multivariate Gaussian distribution to use as a reference I use [this Scipy API](http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.multivariate_normal.html).
We train the second-order model with the [numpy `lstsq` method](http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq).
We then compute the gradient on our own.
As we define the ordering of the features, the fastest way to compute the gradient as a partial derivative is to recall the ordering of these features, and a pre-computed formulation of the gradient based on the partial derivative we compute by hand.

### Use Case

To test whether this actually converges to the maximum of a distribution, we feed it an expected Gaussian curve, and ask the model to find its center.
We generate a two-dimensional Gaussian curve with a height at 5.
To make sure that each of the corners yield a different enough score to yield ascent to begin with, we offset the Gaussian from the center of the space of possible input values.
We plot a contour diagram of this with contours at 1, 2, 3, 4, and 5.
Then we feed these approximate values to our algorithm whenever it requests a score.

We measure a couple of observations:
1. How many iterations does it take for the algorithm to converge to the maximum?
2. What is the model's error from the actual model at each step?
3. How long does it take for the algorithm to get a good-looking surface (as judged by the consecutive contours)?
4. What are the magnitudes of the first and second-order coefficients for the surface at each tutorial?

### Expected Outcome

It takes us about 20 iterations to converge.
However, we do converge to the global maximum, or at least within the ring of the value of 4 for the Gaussian.
The model's error never gets to be less than 20% of the actual Gaussian's volume, but it is less than 50%.
The coefficients change from first-order dominant to second-order dominant after about 2 ascents.

## Notes

### Observations

We are seeing some really annoying behavior where when we try to train the second-order model, sometimes we end up with a minimax.
In several of the models we could come up with, we have unbounded growth on the fringes.
This makes the gradient high magnitude and contributes to jumps.
There are several things we can do to improve our system's ability to handle this type of prediction:
* Limit the type of second-order approximations to just upside-down parabaloids
* Limit the type of approximation to Gaussian
* Try to reduce the possibility of getting a minimax, by sampling not only at the corners, but the midpoints of the edges, which prohibits high-value parts of the distribution getting predicted around these midpoints
* Put an absolute maximum on the allowed jump size

We have iterated through several different APIs for optimization:
* `leastsq` doesn't do more than 8 iterations, and seems to not change the parameters
* `curve_fit` optimizes the parameters (as long as `max_fev` is set to 10000), but won't guarantee keeping the covariance matrix positive semi-definite.
* `sklearn.mixture.GMM`: this algorithm is only built to fit a Gaussian to a set of observations sampled from a random variable, and can't fit probability predefined probability densities at different points.  (Though in a non-active learning context where all of the densities were available ahead of time, you could approximate this effect by scaling the number of observations at a given point by the intended probability density.)

### Technical Improvements

### Research Ideas
 
#### Potential Weaknesses for this in practice

There are a few things that this model might not handle well
* Inconsistent or noisy user-provided ratings.  This might result in convergence to a non-maximum (as high scores are given too early)
* How do we make sure that it doesn't get stuck at the corners of the configuration space, if people want parameters outside of the configuration space?
