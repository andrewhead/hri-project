#! /bin/sh

UTL=../../deps/vowpal_wabbit/utl
python $UTL/active_interactor.py localhost 6075 data/unlabeled.dat -v --watch ./out.model --models-dir models
