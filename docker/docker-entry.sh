#!/bin/bash

(
  cd /project
  if [[ ! -r mktechdocs.conf ]] ; then
    mktechdocs init <<< $(echo y)
    RV=$?
  else
    mktechdocs
    RV=$?
  fi
  exit $RV
)
RV=$? ; [[ $RV != 0 ]] && exit $RV

exit 0
