#!/bin/bash

wait_for_zookeeper() {
  echo "Проверка доступности Zookeeper..."
  while ! nc -z zookeeper 2181; do
    sleep 1
  done
  echo "Zookeeper доступен."
}

wait_for_zookeeper

echo "Запуск Kafka..."
kafka-server-start.sh /path/to/kafka/config/server.properties