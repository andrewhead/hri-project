# Planning 2: Algorithm, its Inputs and Outputs

## Algorithm basis

### Input

Single observations about the current robot performance.
May be provided in the form of a Likert scale.

### Output

Cost function that attempts to predict the user.
And, more importantly, a configuration at which this cost function is a minimum.

### Routine

#### Option 1: Related this back to maximum entropy

We do similarly to the work on maximum entropy where we assume that P(q) = e^-(U(q)).
The cost function U is estimated based on the ratings of the human.
In this way, the cost function can be seen as a predictor of what the human will guess.

While an early examples provided may seek to explore the space, later examples will likely be aimed towards providing maximum probability (lowest cost) examples.

#### Option 2: Multivariate Gaussian (GMM in one dimension)

Multivariate Gaussian.
Estimate the mean based on the scores received so far.
However, GMM are usually initialized with 1-2 demonstrations.
This means that we need to be able to seed some initial demonstration and get ratings on them.

## Related Work

1. Multi-thresholded Approach to Demonstration Selection for Interactive Robot Learning
2. Confidence-Based Policy Learning from Demonstration Using Gaussian Mixture Models
3. Maximum Entropy Inverse Reinforcement Learning
