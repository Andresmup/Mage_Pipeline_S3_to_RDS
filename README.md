# **PIPELINE CON MAGE S3 -> RDS**


👋 Bienvenido/a a mi guía sobre cómo hacer un pipeline para procesamiento de datos utilizando Mage.

🔥 En esta demo transformaremos los datos de un Bucket S3  para cargarlos en una base de datos RDS Postgres en AWS. 🔥

🌐 Toda la información sobre Mage la puedes encontrar en https://docs.mage.ai/introduction/overview



![alt text](https://github.com/Andresmup/Data_Engineering_Practice/blob/main/PIPELINE.png?raw=true)




## ➡️ Preparación entorno

1.   Lo primero que se necesita en tener instalado, y abierto **Docker**.
2.   Necesitamos una carpeta donde se alojara el proyecto. Y abrir una terminal allí.
3.   El primer comando será para clonar el template.
```
git clone https://github.com/mage-ai/compose-quickstart.git mage-quickstart
```
4.   Una vez listo, siguen.
```
cd mage-quickstart
cp dev.env .env
rm dev.env
```
5.   Siempre conviene tener la última versión....
```
docker pull mageai/mageai:latest
```
6.   Y ahora solo hay que lanzar Mage.
```
docker compose up
```
7. Si todo funcionó bien en **http://localhost:6789** nuestra aplicación esta ejecutándose.

## ➡️ Código de los bloques

🐍 Utilizando bloques de código en Python conseguiremos: 🐍

✅ Cargar los datos almacenados en un Bucket S3 de AWS.

✅ Corregir el tipo variable para cada columna.

✅ Limpieza de valores nulos y corrección de valores erróneos.

✅ Cargar los datos en una base de datos RDS Postgres ubicada en AWS.

1.   Bloque Data Loader, donde importamos de S3.

```
@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://s3-pipeline-andresmpaws.s3.amazonaws.com/2023-citibike-tripdata.zip'

    dtype_mapping = {
        'ride_id': str,
        'rideable_type': str,
        'start_station_name': str,
        'start_station_id': str,
        'end_station_name': str,
        'end_station_id': str,
        'start_lat': float,
        'start_lng': float,
        'end_lat': float,
        'end_lng': float,
        'member_casual': str
    }
    parse_dates = ['started_at','ended_at']
    return pd.read_csv(url, sep = ",", compression = "zip", dtype=dtype_mapping, parse_dates=parse_dates)
```
2.   Bloque Transformer procesador de nulos.

```
@transformer
def transform(data, *args, **kwargs):

    null_counts = data.isnull().sum()
    print(f"Preprocessing rows with null values:\n{null_counts}")

    return data.dropna()
```

3.   Bloque Transformer corrección valores incorrectos.

```
@transformer
def transform(data, *args, **kwargs):
    data_filtered = data[~data['start_station_id'].astype(str).str.contains('\.') & ~data['end_station_id'].astype(str).str.contains('\.')]
    data = data_filtered.copy()
    return data

```
4.   Bloque Data Exporter a Postgres.

```
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    schema_name = 'citi_bike'  # Specify the name of the schema to export data to
    table_name = 'citi_bike_data_2023'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'rds'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```
## ➡️ Conexión a RDS
Para que mage pueda conectarse a la base de datos, en este caso es Postgres en RDS de AWS; hay que crear o editar el archivo ```io_config.yaml```. 

Donde agregaremos esta sección y completaremos.

```
rds:
  # PostgresSQL
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: NombreBaseDatos
  POSTGRES_SCHEMA: "{{env_var('POSTGRES_SCHEMA')}}" # Optional
  POSTGRES_USER: UsuarioBaseDatos
  POSTGRES_PASSWORD: ContraseñaBaseDatos
  POSTGRES_HOST: HostBaseDatos
  POSTGRES_PORT: 5432 #Valor default

```

--------------------------------------------------------------------------------

♻️ Los bloques creados pueden ser utilizados en otro pipeline.

🗂️ Mage ofrece múltiples posibilidades para conectarse con diferentes fuentes de datos, y exportarlas a varios servicios.

📜 Puedes modificar los bloques para que se adapten a tus necesidades.

--------------------------------------------------------------------------------

💬 Gracias por visitar mi repositorio. Si tienes alguna duda o sugerencia, no dudes en contactar. 💬

👨‍💻 Andrés Muñoz Pampillón
