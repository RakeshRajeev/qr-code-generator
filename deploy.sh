#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Build the image
docker build -t $DOCKER_USERNAME/qr-generator:$TAG .

# Push to Docker Hub
docker login
docker push $DOCKER_USERNAME/qr-generator:$TAG

# Deploy using the main docker-compose file
docker-compose pull
docker-compose up -d
