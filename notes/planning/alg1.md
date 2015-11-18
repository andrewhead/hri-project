# Algorithm 1: Active Learning for Gaussians

## Problem Formulation

All of this is based on Cohn et al. 1996.

### The process of selecting a query

1. Compute the formula for σ[y^]^2(x) given the current model
2. Compute the formula for P(y~|x~)
3. Compute the formula for σ~[y^]^2(x) given #1 and x~
4. 

### A more hacky way of going about it

1. Sample possible queries (x~,y~) using Monte Carlo method
2. Train new model with each one
3. Compute variance of model for each one
4. Select query (x~,y~) as that which creates the model with lowest variance

### A more formal framing

The below might be unnecessary, but may be useful if we're going for picking the absolutely optimal next query.

#### Task

    x~* = argmin[x~] <σ[y^]^2>
    x~* = argmin[x~] E[ D ∪ (x~,y~) ] [ σ[y^]^2|x] ]

In other words, query a new point that minimizes the expected variance of the model.
As a convex optimization problem, this would look like:

    min[x~] (y^ - mean(y^)) ^ 2

#### Assumptions

* We have some function P(y~|x~) that predicts the probability of observing a y for a queried point x~
* We have some method of computing σ[y^]^2 given training dataset D

#### Fleshing out the Algorithm

##### P(y~|x~)

To compute an expected y~ for an x~, we can use the model we've developed so far.
We could try to compute the expected value of y for an x~ in a circular way, assuming a normal distribution:

    E[y|x] = ∫[y] y P(y|x) dy
    P(y|x) ≈ A * exp(-(y - E[y|x])^2 / σ[y|x])
    σ[y|x] = (some estimation elsewhere in Cohn et al. 1996?)

Otherwise, perhaps we forget P(y~|x~) altogether and just fetch the expected value for x by computing the model at that point.

    E[y|x] = y^(x)

where y^ is the prediction provided by our model.
