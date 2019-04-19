#!/bin/bash

(
  cd /project
  if [[ ! -r mktechdocs.conf ]] ; then
    mktechdocs init <<< $(echo y)
  else
    mktechdocs
  fi
)

