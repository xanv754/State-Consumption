# MODULE: DATABASE
> **DOCUMENTATION VERSION: EN** 

...

> **DOCUMENTATION VERSION: ES** 

Este modúlo se encarga de manejar la base de datos de los Nodos de la red. Su función es poder proporcionar un archivo de tipo `.xlsx`, `.csv` (delimitado por `;`) o `.txt` (delimitado por `,`) con los siguientes datos:

- IP: IP del Nodo
- Estado: Estado del Nodo
- Nodo: Nombre del Nodo (también llamado: Central)

El archivo debe tener una única columna para cada uno de los datos anteriores, de manera que el archivo se pueda leer con un solo comando.

**Importante:** Las columnas no deben contener palabras clave como **IP**, **Estado** o **Nodo** en el nombre a menos que sea la columna precisa con dicha información, ya que estas palabras se usarán para identificar las columnas específicas.

    ✅ Numero, Estado, Nombre del Nodo, IP, Otra columna sin palabra clave
    ❌ Numero del Nodo, Estado del Nodo, Nombre del Nodo del Estado, IP del Nodo, Otra columna con palabra clave

## Requerimientos
Librerías existentes en el archivo `requirements.txt` de este proyecto para su fácil instalación.

## Variables de Entorno
Se necesita proporcionar un archivo `.env` con las siguientes variables de entorno:

**Obligatorias**

- `URI`: URI del servidor de MongoDB
- `DB`: Nombre de la base de datos
- `MASTERNODO_PATH`: Ruta del archivo de datos

**Para las pruebas unitarias** 

- `FILE_CONTENT_EXCEL`: Contenido del archivo `.xlsx` de prueba
- `FILE_CONTENT_CSV`: Contenido del archivo `.csv` de prueba
- `FILE_CONTENT_TXT`: Contenido del archivo `.txt` de prueba

## Uso
Al tener un nuevo archivo `MASTERNODO` para actualizar la base de datos, solo basta con añadir el módulo de `database` al PYTHONPATH para poderlo ejecutar.

```bash
python -m database
```

De otra forma, se puede ejecutar directamente el archivo:
```bash
python database/__main__.py
```

## Pruebas Unitarias
Si se desea ejecutar las pruebas unitarias, se debe ejecutar el archivo de testing:
```bash
python -m pytest database/test_files.py
python -m pytest database/test_finds.py
python -m pytest database/test_inserts.py
```
También se puede ejecutar una función de prueba individual:
```bash
py -m pytest database/test_files.py::test_read_excel
```

## Modelos

#### `database/entity/node.py`

Representa un Nodo de la red.
