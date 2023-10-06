#!/bin/bash

MACHTYPE=`uname -m`

UPAR="--build-arg UID=`id -u` --build-arg GID=`id -g`"

docker build $UPAR -t marrtino:system -f Dockerfile.system . && \
docker build $UPAR -t marrtino:noetic_system -f Dockerfile.noetic_system . && \
docker build -t marrtino:orazio -f Dockerfile.orazio . && \
docker build -t marrtino:base -f Dockerfile.base . && \
docker build -t marrtino:teleop -f Dockerfile.teleop . && \
docker build -t marrtino:navigation -f Dockerfile.navigation . && \
docker build -t marrtino:vision -f Dockerfile.vision . && \
docker build -t marrtino:speech -f Dockerfile.speech . && \
docker build -t marrtino:mapping -f Dockerfile.mapping . && \
docker build -t marrtino:pantilt -f Dockerfile.pantilt .



#docker build $UPAR -t marrtino:objrec -f Dockerfile.objrec .

