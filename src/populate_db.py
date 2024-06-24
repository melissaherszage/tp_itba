import pandas as pd
import requests
from sqlalchemy import create_engine
import os
import time

# Esperar a que la base de datos esté lista
time.sleep(10)


# Descargar el archivo CSV desde Internet
url = 'https://opendata.maryland.gov/api/views/un65-7ipd/rows.csv?accessType=DOWNLOAD'
response = requests.get(url)
csv_file_path = '/app/data/monthly_vehicles_sales.csv'

# Guardar el archivo CSV
with open(csv_file_path, 'wb') as file:
    file.write(response.content)

# Leer el archivo CSV
df = pd.read_csv(csv_file_path)

# Renombrar las columnas del DataFrame para que coincidan con los nombres de las columnas en la tabla de la base de datos
df.rename(columns={
    "Year ": "created_year",
    "Month ": "created_month",
    "New": "new_vehicles_sales",
    "Used": "used_vehicles_sales",
    "Total Sales New": "new_vehicles_tpv",
    "Total Sales Used": "used_vehicles_tpv"
}, inplace=True)

# Datos de conexión a la base de datos
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'tp_data123')
db_host = os.getenv('DB_HOST', 'postgres')  # 'db' es el nombre del servicio de la base de datos en Docker Compose
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'tp_data_itba')

# Crear la cadena de conexión
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

# Nombre de la tabla
table_name = 'monthly_vehicles_sales'

# Lista de columnas a insertar (excluyendo 'id')
columns_to_insert = ['created_year', 'created_month', 'new_vehicles_sales', 'used_vehicles_sales', 'new_vehicles_tpv', 'used_vehicles_tpv']


# Insertar el DataFrame en la tabla
df.to_sql(table_name, engine, if_exists='append', index=False)

print("Datos insertados exitosamente.")
