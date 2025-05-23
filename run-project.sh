#!/bin/bash

# Chạy backend
echo "Starting backend..."
cd ./be || exit
docker-compose up -d
cd ..

# Chạy frontend
echo "Starting frontend..."
cd ./fe || exit
# Xoá image nếu tồn tại
docker image rm web_fe

docker-compose up -d  --build
cd ..

# Mở trình duyệt (chỉ hoạt động trên Linux với xdg-open hoặc Mac với open)
echo "Opening http://localhost:8080 in your browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
elif command -v open &> /dev/null; then
    open http://localhost:8080
else
    echo "Please open your browser and go to http://localhost:8080"
fi
