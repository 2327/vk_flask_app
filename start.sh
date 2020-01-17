#!/usr/bin/env bash
app="vk_app:flask"
app_ws="vk_app_ws:flask"

docker build -t ${app} . -f Dockerfile.site
docker build -t ${app_ws} . -f Dockerfile.ws

## TODO: usage() { echo "Usage: $0-f" 1>&2; exit 1; }
#
#while getopts ":f" o; do
#    case "${o}" in
#        f)
#            docker run -ti -p 8000:8000 \
#              --rm --name=${app%%:*} \
#              -v $PWD:/app ${app}
#            docker run -ti -p 8001:8001 \
#              --rm --name=${app%%:*} \
#              -v $PWD:/app ${app_ws}
#            ;;
#        *)
            docker run -d -p 8000:8000 \
               --name=${app%%:*} \
              -v $PWD:/app ${app}
            docker run -d -p 8001:8001 \
               --name=${app_ws%%:*} \
              -v $PWD:/app ${app_ws}
#            ;;
#    esac
#done
