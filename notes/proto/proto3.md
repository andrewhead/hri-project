# Prototype 3: Achieving a variety of raster effects on laser cut materials

## Overview

### Purpose

According to "Laser Cut Like a Boss", a variety of different appearances can be achieved when laser cutting a material by varying the parameters of the laser.
See this manual for suggestions on how power, speed, frequency, and resolution can be altered to achieve different raster appearances and cutting outcomes.
We're interested in documenting a variety of different appearances of rasters on three different materials.
In addition, we're interested in documenting whether flame in actuality occurs during any of these tests, which obviously we need to avoid when exploring parameter spaces for a machine.

### Summary

## Procedure

We work with scrap for the following materials:
* cardboard
* soft wood
* color acrylic

For each of these materials, we are interested in producing the following:
* an engraving with the default settings
* a low-resolution engraving
* a high-resolution engraving
* a low-power engraving
* a high-power engraving

We are also interested in achieving the following affects:
* dark acrylic engraving
* melted/smooth acrylic engraving

### Expected Outcome


## Notes

### Observations

#### Round 1: Gradient Circle

We engrave a single circle that has a gradient from completely black to completely white from left to right.
This was designed to be only .75-inch for the speed of engraving.
Each engraving was done one after another in a row so that we could compare the appearance after each one.

Column-indexes start at 1.

Columns 1-4 for the acrylic all look like they're the same.

Original settings for color acrylic:
* Power: 27.8%
* Speed: 100%
* Density: 80.0%
* PPI: 500

Color Acrylic:
* Original settings: Power=27.8%, Speed=100%, Density=80.0%, PPI=500
* Low speed ends up leaving a lot of "gunk" on the engraving (column 7)
* As far as I can tell, the density stays the same regardless of the resolution or density settings.
Actually, on second inspection it looks like it works---it just has the same resolution for the leftmost (lightest) points in the gradient.

Cardboard (using construction paper as the initial preset from the ULS UI).

| Material | Configuration | Col Index | Power (%) | PPI | Bad? | Notes |
|----------|---------------|-----------|-----|----------|----|------|
| cardboard | default    | 1 | 7.8 | 500 | No |  |
| cardboard | low-res    | 3 | 27.8 | 500 | No | Engraving appears for the lighter colors, there's char for the darker colors |
| cardboard | high-res   |  |  |  |  |  |
| cardboard | low-power  |  |  |  |  |  |
| cardboard | high-power | 2 | 27.8 | 100 |  |  |
| color acrylic | default    | 1 | 27.8 | Density=80 | No |  |
| color acrylic | low-res    | 4 | 27.8 | Density=20 | No |  |
| color acrylic | high-res   |  |  |  |  |  |
| color acrylic | low-power  | 10 | 57.8 | 1000 | No | Looks darker | 
| color acrylic | high-power |  |  |  |  |  |
| color acrylic | smooth     |  |  |  |  |  |
| color acrylic | dark       |  |  |  |  |  |
| soft wood | default    |  |  |  |  |  |
| soft wood | low-res    |  |  |  |  |  |
| soft wood | high-res   |  |  |  |  |  |
| soft wood | low-power  |  |  |  |  |  |
| soft wood | high-power |  |  |  |  |  |

**Then we aborted the investigation of this table in favor of faster iteration.**

#### Round 2: Solid Black Square

For the next round of observations, we instead concentrate on a purely black square that is .5" across.
This is to reduce the amount of time that it takes to raster, and to make changes in resolution and frequency more pronounced.
Each raster takes around 50s to perform.

For soft wood, we started with the Wood → Soft Wood → General Soft Woods preset for VLS3.50.

| Material | Configuration | Col Index | Power (%) | Speed (%) | PPI | Bad? | Notes |
|----------|---------------|-----------|-----------|-----------|-----|------|-------|
| cardboard | default    |  |  |  |  |  |  |
| cardboard | low-res    |  |  |  |  |  |  |
| cardboard | high-res   |  |  |  |  |  |  |
| cardboard | low-power  |  |  |  |  |  |  |
| cardboard | high-power |  |  |  |  |  |  |
| color acrylic | default    |  |  |  |  |  |  |
| color acrylic | low-res    |  |  |  |  |  |  |
| color acrylic | high-res   |  |  |  |  |  |  |
| color acrylic | low-power  |  |  |  |  |  | 
| color acrylic | high-power |  |  |  |  |  |  |
| color acrylic | smooth     |  |  |  |  |  |  |
| color acrylic | dark       |  |  |  |  |  |  |
| soft wood | default    | 1 | 100 | 81 | 500 | no | goes some depth into the wood---you can feel the depth |
| soft wood | low-res    | 2 | 100 | 81 | 10 | no | looks slightly lighter, but doesn't look much different |
| soft wood | low-res 2  | 6 | 100 | 81 | 10 | no |  |
| soft wood | high-res   | 3 | 100 | 81 | 1000 | no | appears about the same to the past two |
| soft wood | low-power  | 4 | 20 | 81 | 500 | no | much lighter, no perceivable edge from far away |
| soft wood | high-power | 5 | 100 | 20 | 500 | yes (brief) | brief flame towards the beginning.  Major scorching, especially at the top |

#### Round 3: Large image raster

There may be some causes that we can't see the difference in rastering.
Maybe we need an image with greater variance, or a much greater raster area altogether.
So, I follow up with an image of a red ribbon.
This has some grayscale variance, and is about 1.5in x 3in.

| Material | Configuration | Col Index | Power (%) | Speed (%) | PPI | Bad? | Time | Notes |
|----------|---------------|-----------|-----------|-----------|-----|------|-------|
| soft wood | default    | 1 | 100 | 81 | 500 | no | ~5:02 | One important aspect of the most important raster is that it would helpful to do it much faster. |
| soft wood | low-res    | 2 | 100 | 81 | 10 | no | ~5:02 | This didn't seem to go any faster than last time.  Looks slightly darker, but the density of pixels appears just about the same |
| soft wood | fast       | 2 | 100 | 100 | 500 | no | 5:25 | Took *longer* than the lower speed.  Maybe because the time to reverse the direction of the laser cutter was larger than before, and that was the limiting factor.  But, appears lighter than before. |

Note that as the ribbon design is much more vertical than horizontal, the speedups from 81% to 100% speed may be greater if rastering was done in a vertical direction instead of a horizontal direction.

#### Round 4: Engraving

The [VersaLASER User Guide](http://www.denfordata.com/bb/download/file.php?id=1782) states that resolution (PPI) only affects vector cutting and marking.
So, now we'll focus on creating a text "Hello" that can be vector marked.
This job will likely finish much faster than the raster jobs.
We will also be able to make a trade-off between resolution and power to get the right depth in the right amount of time.
We also toggle the "speed" parameter to determine whether this setting can actually affect the vector marking speed, as the user guide implies that only power and PPI can affect how vector marking occurs.

| Material | Configuration | Col Index | Power (%) | Speed (%) | PPI | Time | Bad? | Notes |
|----------|---------------|-----------|-----------|-----------|-----|------|------| ------|
| cardboard | default    |  |  |  |  |  |  |  |
| cardboard | low-res    |  |  |  |  |  |  |  |
| cardboard | high-res   |  |  |  |  |  |  |  |
| cardboard | low-power  |  |  |  |  |  |  |  |
| cardboard | high-power |  |  |  |  |  |  |  |
| cardboard | low-speed  |  |  |  |  |  |  |  |
| cardboard | high-speed |  |  |  |  |  |  |  |
| color acrylic | default    | 1 | 16.4 | 24 | 1000 | ? | No | Just barely visible.  Can be felt.  Can only be seen in reflective light.  |
| color acrylic | low-res    | 2 | 16.4 | 24 | 50 | 0:20 | No | Arguably more visible.  Visible dots.  Laser made funny noises. |
| color acrylic | high-res (skipped, default is max PPI)  |  |  |  |  |  |  |  |
| color acrylic | low-power  | 3 | 5 | 24 | 1000 | 0:21 | No | Looks shallower than 1 |
| color acrylic | high-power | 4 | 50 | 24 | 1000 | ? | No | Melting on the edges of characters.  Outline more visible from a distance. |
| color acrylic | low-speed  | 5 | 16.4 | 6 | 1000 | ? | No | Again, some melting on the edges.  Doesn't seem as deep as with low power. |
| color acrylic | high-speed | 6 | 16.4 | 70 | 1000 | 0:20 | No | Very light.  Appears like 3 (low-power). |
| color acrylic | smooth     |  |  |  |  |  |  |  |
| color acrylic | dark       |  |  |  |  |  |  |  |
| soft wood | default    | 1 | 20.4 | 24 | 500 | 0:21 | No | A little scorching to the top and bottom |
| soft wood | low-res    | 2 | 20.4 | 24 | 50 | 0:21 | No | Dots are very pronounced.  No scorching.  Made funny noises. |
| soft wood | high-res   | 3 | 20.4 | 24 | 1000 | 0:21 | No | Lettering looks darker and thicker than in the first trial.  Some scorching. |
| soft wood | low-power  | 4 | 5 | 24 | 500 | ? | No | About at faint as 2, but much smoother. |
| soft wood | high-power | 5 | 40 | 24 | 500 | 0:21 | No | Darkest so far.  And the most scorching.  |
| soft wood | low-speed  | 6 | 20.4 | 6 | 500 | ? | No | Brightest laser.  Darker and more scorching than 5.  Seems to have taken a very small, marginal amount of time longer than 5. |
| soft wood | high-speed | 7 | 20.4 | 50 | 500 | 0:20 | No | Lighter than 1.  Appears to have taken slightly less time than the default. |

We also note that in the future, a system like this could save configurations from past users, and start with them as a starting point.

### Technical Improvements

### Research Ideas


