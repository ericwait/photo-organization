#!/bin/bash

cd /volume1/homes/ewait/git/programming/photo-organization/src/python
# source /volume1/homes/ewait/py-all/bin/activate
python3 organize.py /volume1/homes/$1/Photos/MobileBackup/ /volume1/photo/RAW/
# find /volume1/homes/$1/Photos/MobileBackup -name "@eaDir" -exec rm -rf '{}' \;
# find /volume1/homes/$1/Photos/MobileBackup -type d -empty -delete
