DROP TABLE IF EXISTS monthly_vehicles_sales;

CREATE TABLE monthly_vehicles_sales (
   id SERIAL PRIMARY KEY UNIQUE NOT NULL,
   created_year INTEGER NOT NULL,
   created_month VARCHAR(256),
   new_vehicles_sales INTEGER,	
   used_vehicles_sales INTEGER,
   new_vehicles_tpv INTEGER,
   used_vehicles_tpv INTEGER
);
