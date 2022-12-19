#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: ./bulk-load-minio.sh ./path/to/folder"
    exit 1
fi


mc alias set thu-ddbs http://localhost:9000 admin password
mc mb thu-ddbs/thu-ddbs
mc mirror $1 thu-ddbs/thu-ddbs
mc anonymous set public thu-ddbs/thu-ddbs
