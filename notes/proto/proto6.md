# Prototype 6: psiTurk implementation test

## Overview

### Purpose

I make and deploy a Mechanical Turk HIT and deploy it through psiTurk.
I do this to make sure that I can make a HIT that collects data into a database, provides conditions in a random order, and uses HTML.

### Summary

## Procedure

### Worker's use case

Wendy the worker is led by the psiTurk ad to a task.
On the opening page, she learns that she will be asked to identify the numbers in ten images.

She reads the text at the top of the page that says
"What number appears in this image?
Please type its value in the text field below."
She sees a (randomly determined) image of a number.
Then she clicks on a field that reads "Enter number here." and types in the number.
She clicks "Next image" at the bottom of the page.

#### Special cases

If Wendy inputs text that is not a number, then she is asked to put in a number.
If Wendy does not input test, then she is asked to put in a number before moving on to the next page.

### Recruiting

Four participants are involved.
The estimated time of their involvement is:

    10 stimuli * 15s / stimulus + 2 minutes startup ≈ 5 minutes

We pay them a worker to aim for an wage of $8 / hour:

    $8 / hour * (1 hour / 60 minutes) * (5 minutes) ≈ $0.67

Therefore, participants are given $0.75 for completing the task.

### Construction

#### Sequences

All workers will get to see ten images, five of the number 1 and five of the number 2.
Two random sequences of images were pre-computed.
Every time a participant starts participating, they are served one of the two sequences.
The assignment of worker index to sequence is pre-computed for the number of participants that will be recruited.

#### Stimuli

Stimuli were created as different fonts on a small 16x16-pixel canvas in GIMP.
This was to enable the perception of blurring.
By presenting numbers in blurred form to our participants and asking them to identify them, this is like the problem of asking humans to help train a hand-writing recognizer.
I use these stimuli to make the HIT seem at least moderately realistic so that workers adequately pay attention.

#### Metrics to collect

* The sequence that was assigned to the worker
* The start time of the worker
* The end time of the worker
* The time the worker spent on each page
* Judgments: (worker index, sequence_index, text input)

### Expected Outcome

The system works!
I'm capable of viewing each of the listed records in tables in a local database.

## Notes

### Observations

### Technical Improvements

When I process my data, I may need to be aware that in some pathological cases, a participant may have uploaded more than one judgment for a single stimulus.
Also, make sure that I follow appropriate ethics for HITs.

### Research Ideas
 
