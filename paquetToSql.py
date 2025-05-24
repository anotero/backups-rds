import os
import pandas as pd
from sqlalchemy import create_engine
import argparse
import pymysql

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Importar archivos Parquet a MySQL')
    parser.add_argument('--name', required=True, help='Nombre de la base de datos (ej: sdccargo20250521)')
    parser.add_argument('--base-folder', required=True, help='Ruta a la carpeta base donde están las tablas Parquet (ej: data/sdccargo20250521/sdc-cargo)')
    
    args = parser.parse_args()

    # 🔧 Configurá tus datos de conexión MySQL
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DB = args.name

    # Crear la base de datos si no existe
    tmp_conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, port=MYSQL_PORT)
    tmp_conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}`")
    tmp_conn.close()

    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}')

    # 📁 Carpeta donde están tus tablas en Parquet
    BASE_FOLDER = args.base_folder

    # Recorremos cada subcarpeta (una por tabla)
    for table_name in os.listdir(BASE_FOLDER):
        table_path = os.path.join(BASE_FOLDER, table_name)
        
        if os.path.isdir(table_path):
            print(f"\n📦 Importando tabla: {table_name}")
            files = []
            for root, _, filenames in os.walk(table_path):
                for f in filenames:
                    if '.parquet' in f:
                        files.append(os.path.join(root, f))        
            if not files:
                print(f"⚠️  Tabla '{table_name}' no tiene archivos Parquet. Se omite.")
                continue

            try:
                dfs = [pd.read_parquet(f) for f in files]
                df = pd.concat(dfs, ignore_index=True)

                # 💡 Asegurar nombre compatible para MySQL
                if "." in table_name:
                    mysql_table_name = table_name.split(".", 1)[1]
                else:
                    mysql_table_name = table_name
                
                df.to_sql(mysql_table_name, con=engine, if_exists='replace', index=False)
                print(f"✅ Tabla '{mysql_table_name}' importada con {len(df)} filas")
            except Exception as e:
                print(f"❌ Error al procesar tabla '{table_name}': {e}")

if __name__ == "__main__":
    main()
