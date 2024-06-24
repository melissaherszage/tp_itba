import psycopg2
import pandas as pd
import time

# Esperar a que la base de datos esté lista
time.sleep(30)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="tp_data_itba",
    user="postgres",
    password="tp_data123",
    host="postgres"
)

# Función para ejecutar consultas y devolver los resultados como un DataFrame
def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(data, columns=columns)

# Consultas SQL
queries = {
    "Ventas Totales por Año": """
        SELECT created_year, SUM(new_vehicles_sales + used_vehicles_sales) AS total_ventas
        FROM monthly_vehicles_sales
        WHERE created_year < date_part('year',current_date) --elimino el corriente año dado que no terminó y sesga la muestra
        GROUP BY created_year
        ORDER BY 1 desc;
    """,

    "%Crecimiento ventas": """
        WITH ventas AS (
        SELECT
                SUM(CASE WHEN created_year = 2024 AND created_month = 'JAN' THEN new_vehicles_tpv END) as ventas_ultimo_mes_nuevos,
                SUM(CASE WHEN created_year = 2024 AND created_month = 'JAN' THEN used_vehicles_tpv END) as ventas_ultimo_mes_usados,
                SUM(CASE WHEN created_year = 2002 AND created_month = 'JAN' THEN new_vehicles_tpv END) as ventas_primer_mes_nuevos,
                SUM(CASE WHEN created_year = 2002 AND created_month = 'JAN' THEN used_vehicles_tpv END) as ventas_primer_mes_usados
                FROM monthly_vehicles_sales
                WHERE created_month = 'JAN')

                SELECT ventas_ultimo_mes_nuevos::decimal / ventas_primer_mes_nuevos::decimal - 1 AS ratio_evolucion_nuevos,
                        ventas_ultimo_mes_usados::decimal / ventas_primer_mes_usados::decimal - 1 AS ratio_evolucion_usados
                FROM ventas;
    """,
    
    "Mes y Ańo con Más Ventas segun tipo": """
           WITH max_ventas AS (
    SELECT
        created_year,
        created_month,
        new_vehicles_sales,
        used_vehicles_sales,
        RANK() OVER (ORDER BY new_vehicles_sales DESC) AS rank_nuevos,
        RANK() OVER (ORDER BY used_vehicles_sales DESC) AS rank_usados
    FROM monthly_vehicles_sales),

    nuevos AS (
    SELECT DISTINCT
        created_year,
        created_month,
        new_vehicles_sales,
        'nuevos' as type
    FROM max_ventas
    WHERE rank_nuevos = 1),

       usados AS (
    SELECT DISTINCT
        created_year,
        created_month,
        new_vehicles_sales,
        'usados' as type
    FROM max_ventas
    WHERE rank_usados = 1)

    SELECT * FROM nuevos
    UNION
    SELECT * FROM usados
    """,


    "Ingresos Totales por Año": """
        SELECT created_year, SUM(new_vehicles_tpv + used_vehicles_tpv) AS ingresos_totales
        FROM monthly_vehicles_sales
        GROUP BY 1
        ORDER BY 1;
    """,

        "Ańo con mayores ingresos": """
        SELECT created_year, SUM(new_vehicles_tpv + used_vehicles_tpv) AS ingresos_totales
        FROM monthly_vehicles_sales
        GROUP BY 1
        ORDER BY 2 DESC
        limit 1;
    """,

}

# Ejecutar consultas y mostrar resultados
for query_name, query in queries.items():
    df = execute_query(query)
    print(f"\n{query_name}\n")
    print(df.to_string(index=False))

# Cerrar la conexión a la base de datos
conn.close()
