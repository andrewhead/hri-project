# Prototype 2: Running active learning with VW

## Overview

### Purpose

We determine that the VW active learner works at iteratively learning a model from a set of datapoints.

### Summary


## Procedure

### Construction

We randomly generate a set of 30 points that fall above and below the line y = x.
When they fall above the line, they are classified as 1.
When they fall below the line, they are classified as 0.
These points are generated in Python and then output in the [VW file format](https://github.com/JohnLangford/vowpal_wabbit/wiki/Tutorial) without labels to the file `unlabeled.dat`

We start a VW active learner with the command:

    vw --active_learner --port 6075

And then start serving up the unlabeled data with the command:

    active_interactor localhost 6075 unlabeled.dat

We manually provide the label for each of the examples for which a label is requested.
Each time we provide a new label, we print out the list of examples that VW has currently processed and the model that it has learned.
To verify that indeed VW is actively learning and developing a better model with each label it queries, we plot the model and the points it finds with matplotlib.

We work with the vowpal-wepository version tagged `v7.3`, for which all of the tests from `make test` succeed.
We modify the code so that it frequently outputs a model.

#### Finding the location to output the model on each example learned

`simple_label.cc` is a file that outputs status updates through its `print_update` method.
This is called from the `output_and_account_example` method, which appears to query examples for active learning and print status updates.
The call chain in `simple_label.cc` looks like this (from top to bottom of the call stack):

* print_update
* output_and_account_example
* return_simple_example

With the current method of learning, `return_simple_example` is called from `gd.cc`

#### Forcing output of the current model

The method of model output appears to be stored in a field called `text_regressor_name`.
Saving this regressor seems to happen in the `parse_regressor.cc` file with this call stack:

* dump_regressor
* save_predictor
* finalize_regressor

`finalize_regressor` is called from `parse_args.cc` method `finish`.
An initial quick glance at `finalize_regressor` reveals that it doesn't seem to change the state of the regressor---it just prints it out.
The method takes two arguments:
* `all`, a `vw` object that is passed by reference (presumably some global state object)
* `regressor_name`, of type `string`

In `finish`, the `regressor_name` argument is just provided as the `final_regressor_name` field of `all`.
As the `gd.cc` method called `driver` invokes `return_simple_example` with each simple example (see above), and as it has an `all` object, we may be able to force the output of the regressor by calling:

    finalize_regressor(*all, *all.final_regressor_name);

right after `return_simple_example` is called.

### Expected Outcome

We find that indeed, the active learner does what we expect:
it improves the model with each example obtained.
We can see this as the linear model gets closer to the y=x straight diagonal with each example.

## Notes

### Observations

### Technical Improvements

### Research Ideas
 
