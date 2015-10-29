# Outline

## Requirements

1. What do you want to do?
2. What is the key insight?

## Course ambitions

1. T

## Title

Mixed-Initiative Exploration of Fabrication Hardware Parameter Space

## Content

~6 paragraphs of content
* The problem: getting to know a new machine
* Questions
    * How can a robot learn an ideal configuration for a task when no demonstration is given?
    * What are the most efficient subjective inputs to enable fast convergence to the ideal configuration?
* Methods
    * Step 1: Some background into failed tasks
        * Informal interviews with Invention Lab members
        * What types of errors do you encounter with the machines?
        * What has failed in the past?  Tell us about your iteration.  Is there anything that didn't work?
    * Step 2: Implementation of an active learning technique
        * active learning will be performed to derive some type of curve
        * while active learning in its typical contexts has been applied to linear decision boundaries of binary classification, others have explored applying it to continuous values like linear regression
        * I will develop a formulation that makes use of some Gaussian kernel or quadratic formulation
        * recommendation of new examples to try to learn a user's scoring function
    * Step 3: Evaluate methods for input
        * examples of these include: Likert-scale ratings, arrange all indexes in order, better/worse, just pen and paper, or trial and error
        * provide Invention Lab students with stimulus: a rastering they are to achieve
        * algorithm will be run in the background an Wizard of Oz'd onto the interface
        * measures: time taken to perform task
        * Given limits of hardware and time constraints, will probably involve 4-6 testers
        * I have received support from the Invention Lab to do this
* Existing techniques from HRI
    * This robot seems to have different techniques than typical LfD
    * Need to explore a larger space (more like machine learning of a Gaussian model)
* Expected deliverables
    * A catalog of user problems actualizing their plans on the 3D printer
    * An application of active learning-based approach to the hardware
    * A comparison of active learning to iterative and trial-and-error approaches, both observational and time-based

Justification
* First, see "disinterest" below
* Some time in the lab makes it clear that the match between a human and a machine in a creative task require a mutual understanding of each other's intents.  Of course, because the machine is pre-programmed to follow a compiled toolpath, it's the human that needs to do the learning.
* In fact, fabrication machines have idiosyncracies that take a human a long time to learn.  For example, 
* It might not always be the case that a human will read the instruction manual (see MLT), or that they will concretely understand all the parameters that a machine provides

Human-Computer Interaction Practices
* Interviews with some people in the Invention Lab.
    * When did you have to do multiple revisions with a machine?
    * When did a machine not produce for you the exact output that you were expecting?
* An experiment evaluating this method of parameter space exploration
    * Three conditions: iterative space traversal, active learning-based traversal, and manually configuring the parameters

## Revisions

Probably, the robot should give multiple examples at a time, instead of just one.
Batch-based exploration of a configuration space.

Here's a really cool potential experiment to run:
* Have human subjects attempt to *replicate* certain affects we've achieved.  For example, melted, polished look, dark color, or light and sparse.

# Ethos

Virtue (Values)
* This work seeks to unite multiple disciplines---the modern trends in HCI (fabrication and design) and modern trends in robotics (techniques for learning from demonstration)

Craft
* I am well-acquainted with the literature on the topic
    * Mueller and Mark Gross's work on interaction between machine and human
    * Learning from Demonstration literature from HRI class
    * Active learning literature for exploring large spaces of parameters
* I am capable of working with the necessary tools
    * I have access to the Invention Lab and experience with the hardware.  This proposal will focus around a rather simple and fast operation for the machine to do that is hard for the human to get right alone

Disinterest
* I used to think that today's rapid prototyping devices provide a new way of enabling people to build things
* However, some personal evidence makes me think this might not exactly be the case.
* And actually, this isn't just me, either.  Other people in the Invention Lab have had these problems too.
* In fact, due to this long list of items, I'm convinced this is some problem that humans have.  And as long as a human's mental model of the work that the robot will do and the way that it will do it doesn't match anything they know, they'll have to do some exploring to get the robot to do what they want.

# Related Work

For HRI
WirePrint: 3D Printed Previews For Fast Prototyping
The Hybrid Artisans: A Case Study in Smart Tools
inForm: Dynamic Physical Affordances and Constraints
Human-computer interaction for hybrid carving 
Interactive Construction: Interactive Fabrication of Functional Mechanical Devices
Democratizing Technology: Pleasure, Utility and Expressiveness in DIY and Maker Practice
LaserOrigami: Laser-Cutting 3D Objects

For me
Programming With Everybody: Tightening the Copy-Modify-Publish Feedback Loop
Integrating API specific "Instant Example" and "Instant Documentation" display interface in development environment
Saleema Amershi
Max Goldman
