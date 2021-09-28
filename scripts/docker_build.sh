#!/bin/bash

docker build -t joaoferreira051090/kafka-consumer-app:latest ../consumer/.
docker build -t joaoferreira051090/feature-store-api:latest ../feature-store-api/.

docker push joaoferreira051090/kafka-consumer-app:latest
docker push joaoferreira051090/feature-store-api:latest
