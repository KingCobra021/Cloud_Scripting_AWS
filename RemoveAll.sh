#!/bin/bash

image_ids=$(docker images -a -q)

echo "deleting $image_ids images"

docker rmi $image_ids -f
