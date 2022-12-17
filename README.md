# THUDDBS

## Compose

Run the project using the following command
```
docker compose up
```

## Minio

To bulk load articles, images and videos into Minio run the following command
```
./scripts/bulk-load-minio-<linux|macos>.sh /absolute/path/to/data
```

## MongoDB

Initialize the MongoDB cluster using the following scripts
```
./scripts/setup-mongo-cluster.sh
```

To bulk load data into MongoDB run
```
python3 scripts/gen_data_10GB.py
python3 ./scripts/bulk_load_mongo.py
```
