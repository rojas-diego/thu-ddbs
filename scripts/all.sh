docker compose up -d || docker-compose up -d
python3 scripts/gen_data_10GB.py
./scripts/setup-mongo-cluster.sh
python3 ./scripts/bulk_load_mongo.py
