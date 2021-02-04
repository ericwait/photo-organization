#!/bin/bash

cd /volume1/homes/ewait/Documents/programming/photo-organize
# source /volume1/homes/ewait/py-all/bin/activate
python3 organize.py /volume1/homes/$1/Drive/Moments/Mobile/ /volume1/photo/RAW/
find /volume1/homes/$1/Drive/Moments/Mobile -name "@eaDir" -exec rm -rf '{}' \;
find /volume1/homes/$1/Drive/Moments/Mobile -type d -empty -delete
