#!/bin/bash

# Start project
echo "Starting project..."
docker-compose up -d 

echo "The project is being launched using docker, if this is the first time running the project, it may take a few minutes for docker to download the dependencies, please wait"

echo "Please open your browser and go to http://localhost:8080"