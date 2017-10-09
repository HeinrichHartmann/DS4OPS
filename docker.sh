#!/bin/bash

set -e # halt on errors
set -x # print commands
cd `dirname $0`

while [[ "$#" > 0 ]]
do
    case $1 in
        --create)
            docker build . -t ds4ops
            ;;
        --run)
            docker run --rm -it -p 9999:9999 -v $(pwd)/work:/home/jovyan/work ds4ops
            ;;
        *)
            echo "Unknown argument $1"
            exit 1
            ;;
    esac
    shift
done
