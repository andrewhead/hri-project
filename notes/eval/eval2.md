# Evaluation 2: Lab Study with the MIVLS

## Overview

### Purpose

To demonstrate that we closed the loop for testing this algorithm, we need to test its effectiveness.
This preliminary study determines whether this form of mixed-initiative parameter space exploration reduces the number of actions that a user has to perform to get an acceptable job from a laser cutter.

### Summary

## Procedure

### Conditions

* Manual determination of the parameters (SL = self-led)
* Simplex-based (Nelder-Mead) method

### Random Variables

Unfortunately, we only work with particle board for this one pilot study.

### Measures

Efficiency of the interaction method
* Total time taken
* Number of tested configurations
* Time to complete each engraving
* Number of user interface actions
* Efficiency of coverage of the parameter space (measured by dividing the space into a grid and counting up the squares filled)

Safety of the interaction method
* The number of workpieces that caught fire

Human preference (probably skipping these tomorrow)
* Frustration
* Understanding of what the machine was doing
* Boredom
* Engagement
* Feeling that the machine was stupid

### Participants

I recruited six participants.
They were members of my research lab.
It was hoped that they did not have any experience working with lasers in the past, and so wouldn't know what the three parameter bars did.

They were told that we were evaluating a system provided by the Universal Laser Systems company to see which one to implement in the Invention Lab.
This was to hide the that the author had developed these techniques.
Participants were involved for a total of 60 minutes, including a 5-minute briefing, three 15-minute sessions of experimentation with the laser cutter for each of the different conditions, and a 5-minute survey.
If participants did not finish a condition within 15 minutes, they were asked to move on.

#### Invited participants

* Kristin Stephens-Martinez
* Matthew Waliman
* Mitar Milutinovic
* Austin Le
* Hezheng Yin
* Yifan Wu

### Procedure

A user works with a machine to create three workpieces.
In two of the conditions, they are led through a list of possible configurations.
In the third condition, they create the workpiece themselves.

Each cut is performed on a separate piece of material just big enough to hold the engraving.
After each cut, the participant is asked to take the workpiece out, compare it to the example, give it a rating, and decide whether to accept the current workpiece as a reproduction of the example they are provided.

The workstation is instrumented with a light

In the self-led condition:
if they lit the material on fire, then they were asked to stop cutting immediately.
Participants are also allowed to take notes on what they've seen so far.

In the active learning condition:
participants are shown two engravings at a time:
the optimal engraving for the currently learned model, and the next example for improving the model.
participants therefore choose whether to accept the first example, and rate the second example, for each iteration.

In all conditions, participants are encouraged to write down the ratings they have assigned so far.

Participants are told,
"Your task is to reproduce the workpiece here.
Here are some examples of failed attempts.
You will work with the machine to configure the machine to get the cut to reproduce this appearance.
You will choose when you feel that you have accurately reproduced the work."
"The machine is going to attempt to guess what you want.
As you give comparisons, it's going to get closer.
Your task is to provide ratings to help it get closer to the ideal etching.
Then when you're done, click 'Accept'."

After examining each example, the participants hand that example to the experimenter, who marks it with the index of the engraving with a Sharpie pen.
Participants are allowed to refer to previous examples.
In that case, the experimenter provides them with the stack of examples they've created so far.
However, the experimenter will not give them any information about the parameters or ratings that they've given.

A different user interface is provided for the manual and automatic exploration conditions.
<!--
In the manual condition, users are provided with an interface of three sliders that they can alter to etch the material in a different way.
*Before conducting the experiment*, we noted for each material the parameter bounds where the material would catch fire when other parameters were at ~50% capacity.
This parameter for the laser was not allowed to be set to this value in the user interface.
This allowed us to whittle down the space.
-->

#### Choosing the seeds for the simplex

The first four cuts for each participants in the Nelder-Mead condition are the same four sets of settings.
These are:
* high power (100%), high speed (100%), high resolution (1000) (dark and crisp)
* low power (3%), high speed (100%), high resolution (1000) (light and crisp)
* high power (10%), low speed (1%), low resolution (10) (dark and sparse)
We chose starting configurations near the extremes that were highly diverse in appearance.
We also made sure that each of the parameters was shown at their extreme for one or the other conditions.
(Of course, this makes sure that a simplex grows inward instead of outward, which we may also want to test).
We chose three because this is an easy number to rank, and we found 4 to give a high overhead in a 1-D test case.

#### Laser cutter settings

A participant determines the settings for the engraver.
For vector cutting, we predetermine the appropriate settings to be (Power: 60%, Speed: 6%, PPI: 1000).
We also set the system setting that the cutter doesn't home back to zero after each iteration.
The cut is frequently clean, without causing too much combustion of material.

### Expected Outcome

Analysis of the exploration of the design space
* Least time taken: [SL, SA, AL]
* Least number of tested configurations: [SA, SL, AL]
* Least number of user interface actions: [SA, AL, SL]
* Number of failures to converge: [SA, SL]
* Efficiency of coverage of the parameter space: [AL, SL, SA]
* Least distance from ideal configuration: [SA, SL, AL]

Analysis of the interaction experience
* Least number of workpieces that caught fire: [SA, SL, AL]
* Most frustration: [SL, SA, AL]
* I could understand the choices the machine was making: [SA, AL], (no SL)
* I think that the machine was making stupid choices when testing out new configurations: [AL, SA], (no SL)
* I understood what each of the parameters did: [SL], (no SA, AL)
* Most bored: [AL, SA, SL]
* Most engaged: [SL, SA, AL]

## Notes

### Observations

#### Patterns

##### Pen and paper to keep track of the configurations

* P1 and P2

##### A desire to get a good mental model

* P2

#### Participant 1: Hezheng

* Seemed interested in exploring the space of possible configurations by manually tweaking the parameters
* The simplex got stuck with his ratings.  It had nothing better to propose by the 17th example

#### Participant 2: Kristin

* Wants us to figure out people's perception of the linearity / relationships in the space of configurations.  Then map back from people's perceptions of the space onto the machine's perception to allow better exploration
    * For example, how would people insert individual points on a line of possible values (or a continuum)
* Simplex felt like a random walk
* Frustrated that she didn't get to keep her favorite points (though admittedly, we should do this?)
* Kristin had some serious problems with the user interface
    * Not being able to edit the text field in order to set the value of a slider
    * Using swap sort instead of insertion sort

#### Hunches

* Iteration seemed much faster with the simplex-based space guidance.  P2 made it through about 2x as many examples in the same time.  Presumably because she did not have to reason about how her choices affected the engraving

### Limitations

The scenario tested is not entirely realistic:
The laser cutter software offers presets for different materials, yielding our current scenario as likely more inefficient.
If users do not wish to use the presets, they may want to alter the single "power" slider instead of changing the sets of three sliders.
However, I expect that most power users would at some point want to take advantage of the power of customization that the three sliders offer.
Furthermore, I feel that it is representative of the set of settings available for most fabrication machines for advanced usage (grid size, layer density, angle for which to produce support).
There also some materials in the Invention Lab for which no preset exists (for example, cardboard), making it relevant for at least one material to have an efficient way to configure the machine to the right settings.

### Observations

### Errata

### Technical Improvements

### Research Ideas
 
