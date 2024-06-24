# Tp Intermedio Itba

# Ventas Mensuales de Vehiculos 

## Introducción

Este proyecto utiliza Docker Compose para levantar contenedores que manejan la base de datos PostgreSQL, la carga de datos y las consultas de análisis. 

Para el ejercicio se eligió el dataset *MVA Vehicle Sales Counts by Month for Calendar Year 2002 through March 2024* el cual contiene una tabla con la evolucion de ventas tanto en cantidad como en tpv de vehiculos usados y nuevos desde el año 2002 hasta la actualidad. 

### Descripción del dataset


El dataset utilizado en este proyecto contiene información sobre las ventas mensuales de vehículos nuevos y usados desde enero 2002 hasta marzo 2024. Para más detalles, consulte https://catalog.data.gov/dataset/mva-vehicle-sales-counts-by-month-for-calendar-year-2002-2020-up-to-october

**Columnas del Dataset**

Year 	
Month 	
New	
Used	
Total Sales New	
Total Sales Used

El dataset se almacena en un archivo CSV llamado `MVA_Vehicle_Sales_Counts_by_Month_for_Calendar_Year_2002_through_March_2024.csv`.

*Simularemos que MVA es mi empresa y vamos a sacar insights interesantes sobre mi negocio.*

### Qué insights podemos obtener con esta data?

A continuación van diferentes preguntas de negocio que se podrían responder a partir de esta base de datos

	1.  Cómo es la evolución de las ventas de los vehiculos a lo largo de los ańos y cual es la tendencia de dicha evolución?
	2.  Cuál es la diferencia en % de los ingresos generados por la venta de vehiculos el ultimo enero vs. cuando se empezó el negocio?
	3.  Existen patrones estacionales en las ventas de vehículos nuevos y usados?
	4.  Cuál fue el mes con mayor cantidad de ventas de vehículos nuevos y usados en el periodo analizado?	

### Solución de los Ejercicios

El archivo `docker-compose.yml` se configuró para levantar los servicios necesarios en el orden correcto:
- `postgres`: Servicio de base de datos PostgreSQL.
- `init-db`: El script Bash init.sh está diseñado para ejecutar un proceso end-to-end que incluye la creación y configuración de un contenedor PostgreSQL y la ejecución de operaciones DDL mediante la ejecución de un archivo create_tables.sql

El archivo  `docker-compose.override.yml` se usa para extender la configuración definida en docker-compose.yml. Por defecto, Docker Compose busca este archivo adicionalmente al archivo principal y combina sus configuraciones. Esto lo utilizamos para que en diferentes conteinters se corran los scripts de python que populan la base de datos y luego se hacen consultas mediante SQL para contestar preguntas de negocio. 
- `populate-script`: Servicio que carga los datos en la base de datos.
- `reporting-script`: Servicio que ejecuta las consultas después de que los datos hayan sido cargados.

Esto incluye dos scripts:
- `populate_db.py`
- `business_queries.py`

Al ejecutar docker-compose up, Docker Compose combinará ambas configuraciones y levantará tanto el servicio postgres como el servicio python-script.

**Información adicional**

- Los archivos se agrupan en carpetas:
 docker/  *Contiene los Dockerfiles necesarios para construir las imágenes Docker para diferentes servicios.*,
 scripts/ *Scripts para inicialización de la base de datos*
 src/ *Código fuente de la aplicación*
 data/ *Archivos de datos*

- Script de Bash: run_all.sh automatiza el proceso de levantar los contenedores, ejecutar los scripts de inicialización y de consultas, y luego apaga los servicios.


