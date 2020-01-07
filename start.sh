#!/usr/bin/env bash
app="vk_app:flask"

docker build -t ${app} .

docker run -d -p 8000:8000 \
  --rm --name=${app%%:*} \
  -v $PWD:/app ${app}

