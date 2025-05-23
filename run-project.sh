#!/bin/bash

# Start backend
echo "Starting backend..."
cd ./be || exit
docker-compose up -d
cd ..

# Start frontend
echo "Starting frontend..."
cd ./fe || exit
# Remove image if it exists
docker image rm web_fe

docker-compose up -d  --build
cd ..

# Open browser (works on Linux with xdg-open or Mac with open)
echo "Opening http://localhost:8080 in your browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
elif command -v open &> /dev/null; then
    open http://localhost:8080
else
    echo "Please open your browser and go to http://localhost:8080"
fi