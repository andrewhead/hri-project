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

A 64-pt letter "O" was engraved for 5 combinations of power and PPI.
Each of the dimensions increases on a logarithmic scale as we noticed through preliminary experimentation that there is a lot of variation at low values of the settings that gets skipped at the higher values.
* We set the power to 1, 3, 10, 32 and 100 percent. (1 is the lowest it can go)
* We set the speed to 1, 3, 10, 32 and 100 percent.
* We set the resolution to 10, 32, 100, 316, and 1000 PPI (logarithmic scale).

Experiments were performed on a 5.6mm piece of particle board.
Cuts were placed at 20mm apart from each other and arranged in a grid.
Power was varied across the Y-axis, and speed along the X-axis.
Resolution was varied between between consecutive grids.
The machine was instructed to not "home" back to the origin between cuts to speed up the cutting process.

The initial defaults  were set to Natural → Wood → Soft Wood → General Soft Woods in the ULS front-end.
<!--We kept the default speed.-->
The default engraving settings were (Power: 20.4%, Speed: 24%, PPI: 500)

#### Notes from the cutting process

* Several of the engravings were not completed, as they caught on fire for more than one second.  Others, I didn't even run because they would have caught fire based on the trend of increasing flames as I altered the parameters.
* Three of the cuts fell through because the laser cut through the entire material.  These row 4, column 1 for groups 3, 4, and 5.  While I attempted to align the "o" back into the whole that it fell through, I'm not positive the orientation is correct.  For group 5, it looks like the inner ring is facing backward instead of forward as its coloring does not blend with the outer ring.
* Probably for our optimization process, we should set several conditions: examples include try to get a low-res (dashed) engraving, an engraving that with thick lines that did not fall through, an engraving with a smooth but very light line, a fine but dark line that's not charred
* You can load and save laser cutter parameters.  Maybe there's a way to automate this so that I can run a lot of examples at once.
* For the final experiment, we may want to distance these Os even more.  Flames from some cuts appear to char the board near neighboring cuts!
* Lower speeds took a noticably longer amount of time.  I did not record the difference in times.
* For the resolutions of 10 and 32 PPI, the bottom row (max power) looked like it automatically booted up the resolution to the maximum resolution.  Is this an eccentricity in the printer behavior?

#### Preparing the images

I took images of each of the squares of 5x5 configurations that I engraved.
I rotated each in OS X Photos so that all grids were aligned with the X and Y edges.
In Preview, I updated the image of each grid.
To make sure that the coloring of each one was approximately the same, I adjusted the colors by setting the levels with "Auto Levels".
Then I resized each one so that each one could be sliced into a 5x5 grid of smaller images, where one "O" was in the center of each one.
I measured the pixel size of one of the Os for each image.
I determined the width and height with the following equation:

    Width = (O width) * 5 * (291 / 211)

Width and height were equal as each cell in the table was in a square.
The *291* and *211* constants came from measuring the width of an O, with and without the margin on either side.
291 was the pixel width with margins, and 211 was the pixel width without.
This constant makes sure that the width of the cropped image includes space for margins between each O.
We cropped the image to each these dimensions, centering it about the center O of each grid.
Then we split each image into 25 individual Os with with a 128x128 resolution (see the `split.sh` script).

The results of this process are in a file named `images.zip` in Andrew's bDrive.

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
