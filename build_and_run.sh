#!/bin/sh
set -e

echo "Building Docker image 'rss_feeder'..."
docker build -t rss_feeder .

echo "Stopping and removing existing 'rss_feeder' container..."
docker rm -f rss_feeder 2>/dev/null || true

echo "Starting new 'rss_feeder' container..."
docker run -d \
  --name rss_feeder \
  --restart on-failure \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  rss_feeder 

echo "Script execution completed successfully!"
