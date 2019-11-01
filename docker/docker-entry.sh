#!/bin/bash

(
  cd /project
  # We add the echo y business because mktechdocs confirms inits
  mktechdocs $@ <<< $(echo y)
  RV=$?
  exit $RV
)
RV=$? ; [[ $RV != 0 ]] && exit $RV

exit 0
