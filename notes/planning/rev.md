# Revisions

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

