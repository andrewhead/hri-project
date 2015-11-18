# Revisions

## 2015-11-17, Talk with Chelsea

* I could consider robust optimization to handle the noise, but it's probably overkill for so few samples
* Reinforcement learning may be worth considering
* Take a look at the residuals and their spread, and try to find out if there's something wrong in my specification of the learner

## 2015-11-17, Talk with Anca

* Need better algorithm for comparisons
* May need smarter algorithm for steepest ascent
* For comparisons, consider stochastic hill-climbing
* Don't worry too much about usability study.  Get some number on MTurk
* Don't worry too much about stellar results
* Anca is excited by comparisons and ways of handling subjective noise of participants
* Relevant readings: Naelder-Mead, and something regarding "generalized binary search comparison rank nets"

## 2015-11-09--11, UIST ideas

* Contexts where rapid testing of parameters could be helpful
  * Learning how to 3D-print hair (Jerard Laput)
  * Estimating the parameters for melding layers in LayerStacker (Udayan &amp; Tim)

## 2015-11-04, Meeting with Sandy Huang

* There's a 1995-ish statistics paper on wight-based regression with active learning that we can draw from
* How do we incorporate noise into the model?  We may be able to assume a constant amount of noise.  Some alternate models:
  * Throw out the first few scores from users altogether
  * Calibrate to the score range of the user (this might already happen with the Gaussian)
  * Adaptively decrease the first ratings given by the users
  * Adjust ratings based on some initial scores for some sanity ratings
  * Give people exemplars of what is a '1', what is a '3', and what is a '5'
