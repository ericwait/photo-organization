#!/bin/bash

cd /volume1/homes/ewait/Documents/programming/photo-organize
/var/services/homes/ewait/.local/share/virtualenvs/photo-organize-PDu68t8w/bin/python3 organize.py /volume1/homes/ewait/Drive/Moments/Mobile/ /volume1/photo/RAW/
chown -R PhotoStation:PhotoStation /volume1/photo/RAW

