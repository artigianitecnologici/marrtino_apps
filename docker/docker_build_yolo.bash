#!/bin/bash

DOCKERFILE=Dockerfile.yolo
if [ "$1" != "" ]; then
  DOCKERFILE=$1
fi

echo "Dockerfile: $DOCKERFILE"

MACHTYPE=`uname -m`

UPAR="--build-arg UID=`id -u` --build-arg GID=`id -g`"

docker build $UPAR -t marrtino:yolo -f $DOCKERFILE .



