#!/bin/bash

MACHTYPE=`uname -m`

UPAR="--build-arg UID=`id -u` --build-arg GID=`id -g`"

docker build $UPAR -t marrtino:system -f Dockerfile.system . && \
docker build -t marrtino:base -f Dockerfile.base . && \
docker build -t marrtino:robotdog -f Dockerfile.robotdog . && \
docker build -t marrtino:speech -f Dockerfile.speech . 




#docker build $UPAR -t marrtino:objrec -f Dockerfile.objrec .

