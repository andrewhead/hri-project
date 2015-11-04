# Planning 1: Using the Invention Lab Laser Cutter

I chatted with Chris Myers on October 28, 2015.
In particular, I mentioned:

* I am interested in working on an HRI project that helps a person explore the behavior and affordances of a fabrication machine when a technical helper or manual is not easily accessible
* My intended target machine is the laser cutter for rastering.  It has a fast iteration loop, and rastering is a case where several different parameters play together very intricately to achieve a result.
* I'm interested in finding out a way that I can do usability studies carefully and respectfully of the machine.  One way for this may be via a remote desktop where I "Wizard of Oz" the next set of parameters for the machine.

## Discussion

Chris Myers was interested in the project.
He mentioned that we could restrict access to the laser cutter for the sake of a usability study, with advance notice.
Preferably, this would happen before the end-of-semester project rush.
It's also helpful that the Jacobs Institute is getting set up with laser cutters of its own.

We discussed one possible method of enabling a user of the laser cutter to manually express parameters without exposing them to the full interface.
Exposing them to the ULS interface may be daunting, confusing, and may also make them more prone to put the machine in a dangerous configuration.
One possibility to solve this problem is to develop a simple front-end on their or my personal computer.
I monitor the values that they input.
And then I update the ULS interface with this input, within safe ranges of values, before running the machine for the next time.
(And when I get the next configuration from the active learning algorithm, I can)

## Additional ideas (from myself)

### Experiment logistics

Is there a way to capture the most recent cut with a camera and to show a comparison between the current best?
The user may need to open up the laser cutter and take out the work piece to evaluate the quality of the raster, too.
We could also simply place a lamp directly above the laser cutter to let people see the bed more easily.

### Details of active learning scheme

"Better / worse" questions may work better when users are capable of viewing two solutions side by side.
We could also ask users to provide the rank of the current raster compared to all others.
Each of the cuts could also be numbered.
This would allow us to ask "pick the current best".
And "make/revise an ordering of the current best examples".  (Presumably, a person wouldn't have to reorder the full list, but just enter the index of one relative to the other.
We may also be able to use a "branch-and-bound" method of restricting the space of possible "best examples".

We could also simply explore the feasibility of doing warmer-colder style of input to describe how close we are getting to the intended output.
How do people change how they rate "warmth" and "coldness" as time goes on---is there an exponential decay?
Do people simply say "warm" all the time?

### Possible ideas for user input

* Is this point the best so far, or not?
* Rank all of the points you have seen so far
* Is this example better or worse than the last one?
* Is this point good or not?
