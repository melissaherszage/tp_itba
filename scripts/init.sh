#!/bin/bash

# Variables
DB_HOST="postgres"
DB_PORT="5432"
DB_NAME="tp_data_itba"
DB_USER="postgres"
DB_PASSWORD="tp_data123"

# Directorio donde se encuentran los scripts SQL
SQL_SCRIPTS_DIR="/scripts"

# Exportar la contraseña para que psql no la pida
export PGPASSWORD=$DB_PASSWORD

# Esperar hasta que PostgreSQL esté listo para aceptar conexiones
until psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c '\q'; do
  >&2 echo "PostgreSQL está inaccesible - intentando de nuevo en 1 segundo"
  sleep 1
done

# Ejecutar cada script SQL en el directorio
for script in "$SQL_SCRIPTS_DIR"/*.sql; do
  if [ -f "$script" ]; then
    script_name=$(basename "$script")
    echo "Ejecutando $script_name..."
    psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -f "$script"

    if [ $? -eq 0 ]; then
      echo "Script $script_name ejecutado con éxito."
    else
      echo "Error al ejecutar el script $script_name."
      exit 1
    fi
  else
    echo "No se encontraron scripts SQL en $SQL_SCRIPTS_DIR"
    exit 1
  fi
done

echo "Todos los scripts SQL se han ejecutado."
