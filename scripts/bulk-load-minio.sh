#!/bin/bash

mc alias set thuddbs http://host.docker.internal:9000 admin password
mc mirror ./data/minio 

docker exec -d minio1 "/bin/bash /usr/bin/mc config host add srv http://localhost:9000 user pass && /usr/bin/mc mb -p srv/bucket"
