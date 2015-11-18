# Evaluation 1: Patterns of Human Subjective Ratings

## Overview

### Purpose

We determine what surface shapes best fit human ratings of laser cutter output.
We also determine how reliable human ratings are of laser cut quality.

### Summary

## Procedure

### Conditions

#### Per trial

* Laser power
* Resolution

Limited to two variable to enable rapid testing and fewer conditions

#### Per subject

* surface: Gaussian, Gaussian mixture, second-order polynomial

### Random variables

* target depth: shallow, medium, and deep
* material: cardboard, acrylic, particle board

### Measures

#### Determining the quality of fit

* By surface: Quality of fit (% error, variance of error, observe visually)

#### Determining the fallability of using human subject ratings

* By subject: Variance of human ratings overall (Implies polarity / reliability)
* By subject: Variance of human ratings within sample (a few samples are shown several times and spaced at random times in the sequence)
* By subject: Distribution of gradient magnitudes: is it a smooth or jagged increase?  (we want smooth)
* Between subject: Variance of rating for an image.  Shows whether we can adapt models found by different people to the same task.

### Follow-Up Tests

To maximize the applicability to eventual use of steepest ascent, we do the following:
* in one of the conditions, we show samples as if they were shown in steepest ascent (from not very close in one of the corners to very close)

### Artifacts

A 96-pt letter "O" was engraved for 5 combinations of power and PPI.
We set the power to 1, 25, 50, 75 and 100 percent. (1 is the lowest it can go)
We set the resolution to 10, 32, 100, 316, and 1000 PPI (logarithmic scale).
They were placed at 25mm apart from each other and arranged in a grid.
Power was varied across the Y-axis, and resolution along the X-axis.
The initial defaults  were set to Natural → Wood → Soft Wood → General Soft Woods in the ULS front-end.
We kept the default speed.
The default engraving settings were (Power: 20.4%, Speed: 24%, PPI: 500)
Experiments were performed on a 5.6mm piece of particle board.

### Apparatus 1: Fitting surfaces to random sampling

Subjects are shown all examples in a random order for each of three rounds.
For each round, the random order is distinct.
The participant is not told that the next round is starting.

### Apparatus 2: Fitting surfaces to steepest ascent

Subjects are shown examples that proceed on a trajectory from not good to ideal.
Assuming that the laser cutter can pick the absolute ideal trajectory, how quickly does the user's ratings converge relative rate of procession towards the ideal configuration?
This relationship suggests how we should scale user feedback in the ideal case to derive a "normalized" rating from the one they offer.
Participants are only allowed to participate in one or the other of these tasks.

### Expected Outcome

We find high variance between the first and second time showing a sample to a person.
We show lower variance between the second and third time a sample is shown.
We find that the Gaussian fits best of all, but there is a high amount of noise.
The Gaussian also fits better with the second round of ratings.
We find that between subject-ratings of examples is high.

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
