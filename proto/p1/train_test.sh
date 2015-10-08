#! /bin/sh

# Train model and output results to file
vw house_dataset -l 10 -c --passes 25 --holdout_off -f house.model

# Store model in a readable format
# vw house_dataset -l 10 -c --passes 25 --holdout_off --readable_model house.model

# Save original feature names
# vw house_dataset -l 10 --holdout_off --invert_hash house.model

# Test on a saved dataset
vw -i house.model -t house_dataset -p /dev/stdout --quiet
