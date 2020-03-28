#!/usr/bin/env bash

SRCDIR=./aligned_labels_openjtalk
OPUDIR=./aligned_labels_openjtalk_jvslike

ls $SRCDIR |\
parallel mkdir -p $OPUDIR/{}/parallel100/lab/mon/

for speaker in $(ls $SRCDIR); do
    find $SRCDIR/$speaker -name '*.lab' |\
    parallel ln {} $OPUDIR/$speaker/parallel100/lab/mon/{/}
done
