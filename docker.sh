#!/bin/bash

set -e # halt on errors
set -x # print commands
cd `dirname $0`

while [[ "$#" > 0 ]]
do
    cmd=$1
    shift
    case $cmd in
        --create)
            docker build . -t heinrichhartmann/ds4ops "$@"
            ;;
        --push)
            docker push heinrichhartmann/ds4ops
            ;;
        --pull)
            docker pull heinrichhartmann/ds4ops
            ;;
        --run)
            docker run --rm -it "$@" \
                   -p 9999:9999 -p 9998:9998 \
                   -v $(pwd):/home/jovyan/work \
                   -v $HOME:/home/jovyan/host/home \
                   -v /:/home/jovyan/host/root \
                   heinrichhartmann/ds4ops
            ;;
        *)
            echo "Unknown argument $1"
            exit 1
            ;;
    esac
    shift
done
