#!/bin/bash

cp Dockerfile.no-groovy Dockerfile
docker build -t mktechdocs-no-groovy:0.0.1 .

cp Dockerfile.groovy Dockerfile
docker build -t mktechdocs-groovy:0.0.1 .

rm -f Dockerfile
