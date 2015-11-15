# Evaluation 2: Lab Study with the MIVLS

## Overview

### Purpose

To demonstrate that we closed the loop for testing this algorithm, we need to test its effectiveness.
This preliminary study determines whether this form of mixed-initiative parameter space exploration reduces the number of actions that a user has to perform to get an acceptable job from a laser cutter.

### Summary

## Procedure

### Conditions

* Manual determination of the parameters (SL = self-led)
* Active learning (AL)
* Steepest ascent (SA)

### Random Variables

To generalize to different materials
* type of material: {particle board, acrylic, cardboard}
* optimized quality: {scorched, melted acrylic, light and sparse}
<!--* depth: {shallow, medium, deep}-->

### Measures

Efficiency of the interaction method
* Total time taken
* Number of tested configurations
* Number of user interface actions
* Efficiency of coverage of the parameter space (measured by dividing the space into a grid and counting up the squares filled)

Safety of the interaction method
* The number of workpieces that caught fire

Human preference
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

#### Intended participants

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

In the self-led condition:
if they lit the material on fire, then they were asked to stop cutting immediately.

Participants are told,
"The machine is going to attempt to guess what you want.
As you give ratings, it's going to get closer.
Your task is to provide ratings to help it get closer to the ideal etching.
Then when you're done, click 'Accept'."

A different user interface is provided for the manual and automatic exploration conditions.
In the manual condition, users are provided with an interface of three sliders that they can alter to etch the material in a different way.
*Before conducting the experiment*, we noted for each material the parameter bounds where the material would catch fire when other parameters were at ~50% capacity.
This parameter for the laser was not allowed to be set to this value in the user interface.
This allowed us to whittle down the space

### Preparation to do

* Get the nozzle attached to the machine.
* Ask Chris: can I work with real-life subjects?

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
 
