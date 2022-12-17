set -e

echo '------- mongo-beijing-config -------'
echo '> Register config servers replica set...'
docker exec -it mongo-beijing-config bash -c "echo '\
    rs.initiate( \
        {_id: \"config-rs\", configsvr: true, members: [ \
            {_id: 0, host: \"mongo-beijing-config\"}, \
            {_id: 1, host: \"mongo-hong-kong-config\"}, \
        ]} \
    )' | mongo"

echo '------- mongo-beijing-shard-1 -------'
echo '> Register beijing shard replica set...'
docker exec -it mongo-beijing-shard-1 bash -c "echo '\
    rs.initiate( \
        {_id: \"beijing-shard-rs\", members: [ \
            {_id: 0, host: \"mongo-beijing-shard-1\"}, \
            {_id: 1, host: \"mongo-beijing-shard-2\"}, \
        ]} \
    )' | mongo"

echo '------- mongo-hong-kong-shard-1 -------'
echo '> Register hong kong shard replica set...'
docker exec -it mongo-hong-kong-shard-1 bash -c "echo '\
    rs.initiate( \
        {_id: \"hong-kong-shard-rs\", members: [ \
            {_id: 0, host: \"mongo-hong-kong-shard-1\"}, \
            {_id: 1, host: \"mongo-hong-kong-shard-2\"}, \
        ]} \
    )' | mongo"

echo '------- mongo-shared-shard-1 -------'
echo '> Register shared shard replica set...'
docker exec -it mongo-shared-shard-1 bash -c "echo '\
    rs.initiate( \
        {_id: \"shared-shard-rs\", members: [ \
            {_id: 0, host: \"mongo-shared-shard-1\"} \
        ]} \
    )' | mongo"

echo '------- Wait ... -------'
echo '> Waiting for cluster to be ready...'
sleep 15

echo '------- mongo-beijing-router -------'
echo '> Register shards in database...'
docker exec -it mongo-beijing-router bash -c "echo '\
    sh.addShard(\"beijing-shard-rs/mongo-beijing-shard-1,mongo-beijing-shard-2\")
    sh.addShard(\"hong-kong-shard-rs/mongo-hong-kong-shard-1,mongo-hong-kong-shard-2\")
    sh.addShard(\"shared-shard-rs/mongo-shared-shard-1\")' | mongo"

echo '------- mongo-beijing-router -------'
echo '> Configure thu-ddbs database and collections...'
docker exec -it mongo-beijing-router bash -c "echo '\
    sh.disableBalancing(\"thu-ddbs.user\")
    sh.disableBalancing(\"thu-ddbs.article\")
    sh.disableBalancing(\"thu-ddbs.read\")
    sh.disableBalancing(\"thu-ddbs.popularRank\")
    sh.disableBalancing(\"thu-ddbs.beRead\")
    sh.enableSharding(\"thu-ddbs\")
    sh.addShardTag(\"beijing-shard-rs\", \"BJ\")
    sh.addShardTag(\"hong-kong-shard-rs\", \"HK\")
    sh.addShardToZone(\"beijing-shard-rs\", \"BJ\")
    sh.addShardToZone(\"hong-kong-shard-rs\", \"HK\")
    sh.addShardTag(\"shared-shard-rs\", \"BJ\")
    sh.addShardTag(\"shared-shard-rs\", \"HK\")
    sh.addShardToZone(\"shared-shard-rs\", \"HK\")
    sh.addShardToZone(\"shared-shard-rs\", \"BJ\")

    sh.shardCollection(\"thu-ddbs.user\", {region: 1})
    sh.splitAt(\"thu-ddbs.user\", {region:\"Beijing\"})
    sh.splitAt(\"thu-ddbs.user\", {region:\"Hong Kong\"})
    sh.moveChunk(\"thu-ddbs.user\", {region:\"Beijing\"}, \"beijing-shard-rs\")
    sh.moveChunk(\"thu-ddbs.user\", {region:\"Hong Kong\"}, \"hong-kong-shard-rs\")

    sh.shardCollection(\"thu-ddbs.article\", {category: 1})
    sh.splitAt(\"thu-ddbs.article\", {category:\"science\"})
    sh.splitAt(\"thu-ddbs.article\", {category:\"technology\"})
    sh.moveChunk(\"thu-ddbs.article\", {category:\"science\"}, \"beijing-shard-rs\")
    sh.moveChunk(\"thu-ddbs.article\", {category:\"technology\"}, \"shared-shard-rs\")

    sh.shardCollection(\"thu-ddbs.read\", {region: 1})
    sh.splitAt(\"thu-ddbs.read\", {region:\"Beijing\"})
    sh.splitAt(\"thu-ddbs.read\", {region:\"Hong Kong\"})
    sh.moveChunk(\"thu-ddbs.read\", {region:\"Beijing\"}, \"beijing-shard-rs\")
    sh.moveChunk(\"thu-ddbs.read\", {region:\"Hong Kong\"}, \"hong-kong-shard-rs\")

    sh.shardCollection(\"thu-ddbs.beRead\", {category: 1})
    sh.splitAt(\"thu-ddbs.beRead\", {category:\"science\"})
    sh.splitAt(\"thu-ddbs.beRead\", {category:\"technology\"})
    sh.moveChunk(\"thu-ddbs.beRead\", {category:\"science\"}, \"beijing-shard-rs\")
    sh.moveChunk(\"thu-ddbs.beRead\", {category:\"technology\"}, \"shared-shard-rs\")

    sh.shardCollection(\"thu-ddbs.popularRank\", {granularity: 1})
    sh.splitAt(\"thu-ddbs.popularRank\", {granularity:\"daily\"})
    sh.splitAt(\"thu-ddbs.popularRank\", {granularity:\"weekly\"})
    sh.splitAt(\"thu-ddbs.popularRank\", {granularity:\"monthly\"})
    sh.moveChunk(\"thu-ddbs.popularRank\", {granularity:\"daily\"}, \"beijing-shard-rs\")
    sh.moveChunk(\"thu-ddbs.popularRank\", {granularity:\"weekly\"}, \"hong-kong-shard-rs\")
    sh.moveChunk(\"thu-ddbs.popularRank\", {granularity:\"monthly\"}, \"hong-kong-shard-rs\")

    ' | mongo"
