# Evaluation 1: Patterns of Human Subjective Ratings

## Overview

### Purpose

We determine what surface shapes best fit human ratings of laser cutter output.

### Summary

## Procedure

### Conditions

Note that the surfaces we want to test are technically a condition in one set of tests we'll run.

#### Generality

To increase the generality, we do the following:
* multiple depths: shallow, medium, and deep
* multiple materials: cardboard, acrylic, particle board

### Measures

We are interested in observing this output:
* How polar are the human ratings?  Measure by the amount of variance is the collection of ratings for each user.
* Which surface type fits best?  Measure by the error of each of the model types fit, and visually.
* How much noise is there in the data?  Report the error for the chosen model type.
* How close to the peak does a configuration have to be to be above "worst"?

The possible surface shapes we want to test for fit are: Gaussian curve, mixture of Gaussians, second-order polynomial with thresholds

### Follow-Up Tests

We also conduct follow-up studies to determine the following:
* Is it likely that subjects will change their rating on a past sample after seeing a few more samples?

To maximize the applicability to eventual use of steepest ascent, we do the following:
* in one of the conditions, we show samples as if they were shown in steepest ascent (from not very close in one of the corners to very close)

### Apparatus

### Expected Outcome

## Notes

### Observations

### Errata

### Technical Improvements

It's possible to calculate expected error per observation based on a user's Likert scale rating.
Assume that a person will round the current actual score to the nearest whole number.
For the rating that they get from this rounding, what is the average distance to the points that get estimated as this rating?
The expected error then depends not on the current rating.
I expect that it does not rely on the covariance matrix, as the ratio of values rounded down to the values rounded up to the value may be the same.
However, I don't know whether that's true before testing it.

### Research Ideas

The fundamental challenge of this application is that human data will be inherently noisy, and there is no clear reference point for collaboration.
