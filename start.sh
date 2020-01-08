#!/usr/bin/env bash
app="vk_app:flask"

docker build -t ${app} .

# usage() { echo "Usage: $0 [-s <45|90>] [-p <string>]" 1>&2; exit 1; }

while getopts ":f" o; do
    case "${o}" in
        f)
            docker run -ti -p 8000:8000 \
              --rm --name=${app%%:*} \
              -v $PWD:/app vk_app:flask
            ;;
        *)
            docker run -d -p 8000:8000 \
              --rm --name=${app%%:*} \
              -v $PWD:/app ${app}
            ;;
    esac
done

