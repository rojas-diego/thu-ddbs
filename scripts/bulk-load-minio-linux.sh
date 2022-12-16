#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "usage: ./bulk-load-minio.sh /absolute/path/to/folder"
    exit 1
fi

docker run --entrypoint "/bin/bash" -v "$1:/data" --network="host" --rm minio/mc "-c" \
    "/usr/bin/mc alias set thu-ddbs http://127.0.0.1:9000 admin password ; \
     /usr/bin/mc mb thu-ddbs/thu-ddbs ; \
     /usr/bin/mc mirror /data thu-ddbs/thu-ddbs ; \
     /usr/bin/mc anonymous set public thu-ddbs/thu-ddbs"
