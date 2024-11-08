#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Этот скрипт должен быть запущен с правами суперпользователя" 
   exit 1
fi

IMAGE_FILE="adindex_dashboard_image.tar"

if [ ! -f "$IMAGE_FILE" ]; then
    echo "Файл с образом Docker не найден: $IMAGE_FILE"
    exit 1
fi

echo "Загружаем образ Docker..."
docker load -i "$IMAGE_FILE"

IMAGE_NAME="adindex_dashboard_image"
if ! docker images | grep -q "$IMAGE_NAME"; then
    echo "Не удалось загрузить образ $IMAGE_NAME."
    exit 1
fi

echo "Запускаем контейнер..."
docker run -d -p 8050:8050 --name adindex_dashboard_container "$IMAGE_NAME"

if [ $? -eq 0 ]; then
    echo "Контейнер успешно запущен!"
else
    echo "Ошибка при запуске контейнера."
    exit 1
fi

# docker ps
