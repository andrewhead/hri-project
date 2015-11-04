#! /bin/bash

PATH=../../deps/vowpal_wabbit/vowpalwabbit:$PATH
vw --active_learning --port 6075 --save_per_pass --readable_model out.model
