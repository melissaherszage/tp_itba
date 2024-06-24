#!/bin/bash

# Construir y levantar los servicios definidos en docker-compose.yml
docker-compose up --build -d postgres

# Esperar a que el servicio de PostgreSQL esté listo
echo "Esperando a que el servicio de PostgreSQL esté listo..."
until docker-compose exec postgres pg_isready -U postgres; do
  sleep 1
done

# Ejecutar el script init.sh
docker-compose up init-db

# Ejecutar el script de carga de datos
docker-compose run --rm populate-script

# Ejecutar el script de consultas
docker-compose run --rm reporting-script

# Apagar los servicios
docker-compose down
