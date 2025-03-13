#!/bin/bash
set -e

# Validate required environment variables
if [ -z "$SERVER_HOST" ]; then
    echo "ERROR: SERVER_HOST is not set"
    exit 1
fi

if [ -z "$SERVER_USER" ]; then
    echo "ERROR: SERVER_USER is not set"
    exit 1
fi

if [ -z "$SSH_PRIVATE_KEY" ]; then
    echo "ERROR: SSH_PRIVATE_KEY is not set"
    exit 1
fi

# Create SSH directory and set permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Write SSH key
echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

# Add host key scanning
ssh-keyscan -H "$SERVER_HOST" >> ~/.ssh/known_hosts

# Test SSH connection
ssh -o StrictHostKeyChecking=no -T "$SERVER_USER@$SERVER_HOST" exit

# If connection successful, proceed with deployment
echo "SSH connection successful, proceeding with deployment..."
cd /app/qr-generator
docker-compose up -d
