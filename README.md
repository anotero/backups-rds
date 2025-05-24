# Importador de Parquet a MySQL

Este script permite importar múltiples archivos Parquet organizados en carpetas a una base de datos MySQL, creando automáticamente la base de datos si no existe y generando las tablas según la estructura de carpetas.

## Requisitos
- Python 3.8+
- MySQL Server
- Acceso a un usuario MySQL con permisos para crear bases de datos y tablas

## Instalación y preparación del entorno

1. **Clona el repositorio o descarga los archivos.**

2. **Crea un entorno virtual con `-m env`:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

## Uso

El script se ejecuta desde la terminal y requiere dos parámetros:

- `--name`: nombre de la base de datos MySQL donde se importarán las tablas. Si no existe, se creará automáticamente.
- `--base-folder`: ruta a la carpeta base donde están las subcarpetas con los archivos Parquet.

### Ejemplo de ejecución

```bash
python paquetToSql.py --name inventario2024 --base-folder data/inventario/inventario2024
```

Esto creará (si no existe) la base de datos `inventario2024` y cargará todas las tablas encontradas en la carpeta `data/inventario/inventario2024`.

### Estructura esperada de carpetas

```
data/
└── inventario/
    └── inventario2024/
        ├── inventario_productos/
        │   └── ...archivos.parquet
        ├── inventario.categorias/
        │   └── ...archivos.parquet
        └── ...
```

- Si la carpeta de la tabla contiene un punto (`.`), el nombre de la tabla será la parte después del punto.
- Si no contiene punto, se usará el nombre completo de la carpeta como nombre de la tabla.

## Notas
- **Sobre el uso de puntos en los nombres de carpeta:** El uso de puntos (`.`) para separar el nombre de la tabla se debe a que los datos provienen de un export de un snapshot de una instancia MySQL de Amazon RDS, que fue obtenido desde S3. Por eso, algunas carpetas pueden tener nombres como `inventario.categorias` y el script toma la parte después del punto como nombre de la tabla.
- **Las credenciales de la base de datos están hardcodeadas en el script** (`root` y contraseña vacía) porque el uso está pensado para entornos locales. Modifícalas si necesitas conectarte a otro servidor o usuario.
- El script ignora carpetas que no contienen archivos Parquet.
- Si una tabla ya existe en la base de datos, será reemplazada.

## Dependencias
Ver `requirements.txt`.

---

**Contacto:** andres.otero16@gmail.com 