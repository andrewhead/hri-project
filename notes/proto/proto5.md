# Prototype 5: Front End for Usability Study

## Overview

### Purpose

I create a prototype of the user interface for controlling the laser cutter parameters for [Evaluation 2](../eval/eval2.md).

### Summary

## Procedure

### Use case

#### Tasks

##### Starting an Experimental Condition

The experimenter enters a number ID for the current participant in a text field.
The experimenter chooses between three anonymous buttons on the screen, labeled "1", "2", and "3".
Each one initializes the interface to the appropriate one for active learning, self-led exploration, or steepest ascent.

*The buttons have no names so that participants are not biased by the name of the condition*

##### Setting the Parameters for Engraving

A participant is shown three sliders.
Each slider has a text label---"Power", "Speed", or "PPI".
As the participant moves the slider, a text box below the slider updates with its current value.
Once the participant is finished editing each of the sliders, they are click on a "Cut" button.
Then the laser cutter performs the cut.

##### Accepting an Example

Participants are asked if they want to accept the current example as a reproduction of the original example provided.
If they click the "Accept" button, they are then asked through a dialogue, "Are you sure?"
If they click "Yes", then the application shows a "Thank you!" page and returns to the main menu.

##### Rating an Example

A participant is shown a seven-point slider.
The right side is labeled "the same".
The left side is labeled "not similar at all".
There is an arrow underneath from left to right that is labeled "Similarity".
When the participant is satisfied with the rating they have assigned, they click on the "Done" button.

##### Going to the next example

A participant is shown a blank screen that says "Wait for the laser cutter to finish engraving".
Once the laser cutter has finished, they click on a button that reads "Rate next example".

### Construction

With each query for a new page, a user uploads their current choices.
The server should be listening for this query and log it with a timestamp, the current example ID, and the user ID immediately.
The server is responsible for maintaining the index of the current example for the user and updating the cookies appropriately.

This is implemented as an HTML and JavaScript web app with jQuery, stored on a Django server.

### Expected Outcome

All of these use cases are quick and straightforward.
Probably, the separate "rate" and "accept" pages are a little tedious to go through every time, but maybe they are easy.

## Notes

### Observations

### Technical Improvements

To help the user orient their ratings relative to previous ones they have given, it could be helpful to draw on the current slider a heatmap of the recent ratings they have given.

### Research Ideas

