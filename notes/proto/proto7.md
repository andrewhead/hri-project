# Prototype 7: Testing Methods for Numerical Optimization

## Overview

### Purpose

We implement the Nelder-Mead and Bayesian optimization methods to determining an optimal configuration.
This is to provide us with at least two methods of mixed-initiative parameter space exploration between a human and a fabrication machine.

### Summary

## Procedure

### Input Mechanisms

The input mechanism for Nelder-Mead is a user-provided ranking mechanism for the samples.
So, we show all N current examples on the plot, and ask for an ordered list of the best to worst.

### Algorithm Implementations

We find an open source implementations of both methods.
[Scipy has an implementation of the Nelder-Mead method](http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#nelder-mead-simplex-algorithm-method-nelder-mead).
We use a 4-point simplex.
One problem with this method is it doesn't allow us to provide rank for sets of points.
Instead, it requests an evaluation of each point.
We then have a couple of options if we want to keep using the simplex method:
Actually try to assign some value on a Likert scale (like we did in [Prototype 4](proto4)).
Display the current numbers that are in the simplex, and ask for the current number's rank relative to these previous points.
Then we assign some numerical value to its cost by amortizing between its nearest neighbors.

Fine, we implement a simplex.
This simplex involves the following steps, based on the [Wikipedia article for Nelder-Mead](https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method):

1. Query the ranks for a set of N starting point points
2. Query the rank of a centroid point, relative to the first N
3. Query the rank of a reflected point, relative to all queried in #1 and #2
4. If the reflected point is the highest rank, query the expanded point and go to 5.  Else, if better than the second-worst point, replace the worst with reflected point and go to #2.  Otherwise, go to #6.
5. If the expanded point is the best point, replace the worst with the expanded point and go to #2.  Otherwise, replace the worst with the reflected point and go to #2.
6. Query the rank of a contracted point.  If better than the worst, replace the worst with the contracted point and go to #2.
7. Compute the reduction for all points but the best.  Go to #2.

* get the rank of the centroi
* compute the reflection, expansion, and contraction
* choose the reflection, expansion, and contraction based on the current ranks of the points
* do a reduction if all else fails

### Front End for Simplex

We enable users to rate examples through a JavaScript front end.
The front-end supports the following tasks:

1. Viewing the current goal
2. Viewing the color of the current centroid (as feedback)
3. Viewing each of the current points of the simplex
4. Rearrange the order of the current simplex points to rank the points
5. Do #4, but with the addition of the reflected, expanded, and contracted points
6. #5 should be served up right after #4.  #4 should be served up right after #5.
7. Once the model has converged, they are shown text that says the system has converged

### Adding graphics

We want to enable one to use our front-end with images.
Some of the following commands were helpful for transitioning our images from [Evaluation 1](../eval/eval1) to this prototype.
In particular, there were some thing (~1 pixel) slices left over from splitting the images.

    rm 1000ppi_{25,26,27,28,29}.png
    # We manually removed 316ppi_{05,11,17,23,29}.png.
    i=0; for f in 316ppi_*; do mv $f 316ppi_`printf "%02d" $i`.png; i=$((i + 1)); echo $i ; done

### Expected Outcome

Nelder-Mead works pretty well without noise.

## Notes

### Observations

#### Methods for evaluating how good each of these methods are

* If we collected measurements from users (for instance, having them rate the quality)

### Technical Improvements

### Research Ideas
 
Objectives for our algorithm for exploration of the input space is:
* Take the fewest number points as possible
    * This probably means a small number of initial input points (but may not need to mean precisely this)
* Take the least amount of time possible
    * This might involve taking the fabrication time into account for the cost function that's approximated
* End up at a sample that best matches the user's intent
