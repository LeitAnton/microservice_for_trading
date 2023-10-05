#!/bin/bash

wait_for_mongodb() {
  echo "Проверка доступности MongoDB..."
  while ! nc -z mongodb 27017; do
    sleep 1
  done
  echo "MongoDB доступна."
}

wait_for_mongodb

echo "Запуск FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8989