# MÓDULO: BASE DE DATOS (DATABASE)
> [English version](./README.md)

Este modúlo se encarga de manejar la creación o actualización de base de datos de los Nodos de la red. Para ello, se debe proporcionar un archivo de tipo `.xlsx`, `.csv` (delimitado por `;`) o `.txt` (delimitado por `,`) con los siguientes datos:

- **Nodo:** Nombre del Nodo o nombre de la central. (Obligatorio)
- **Estado:** Estado de ubicación del Nodo. (Obligatorio)
- **Código Contable:** El código contable asociado al nodo. (Obligatorio)
- **IP:** IP de servicio del Nodo. (Opcional)
- **Region:** Región del estado de ubicación del Nodo. (Opcional)

**Importante:** El archivo debe tener una única columna para cada uno de los datos anteriores, es decir, las columnas no deben contener palabras clave (ej: **Código**, **Estado** o **Nodo**) en el nombre a menos que sea la columna precisa con dicha información, ya que estas palabras se usarán para identificar las columnas específicas.

Ejemplo de las columnas del archivo:

    ✅ Numero, Estado, Nombre del Nodo, IP, Otra columna sin palabra clave
    ❌ Numero del Nodo, Estado del Nodo, Nombre del Nodo del Estado, IP del Nodo, Otra columna con palabra clave

## Requerimientos
Librerías existentes en el archivo `requirements.txt` de este proyecto para su fácil instalación.

## Variables de Entorno
Se necesita proporcionar un archivo `.env` con las siguientes variables de entorno:

- `URI`: URI del servidor de MongoDB
- `DB`: Nombre de la base de datos
- `MASTERNODO_PATH`: Ruta del archivo de datos

## Uso
Al tener un nuevo archivo `MASTERNODO` para actualizar la base de datos, solo basta con añadir el módulo de `database` al PYTHONPATH para poderlo ejecutar:

```bash
python -m database
```

De otra forma, se puede ejecutar directamente el archivo:
```bash
python database/__main__.py
```

Allí se podrá encontrar con el CLI del módulo para obtener información de las diferentes funciones que se encuentran en el módulo.

## Pruebas Unitarias
Si se desea ejecutar las pruebas unitarias, se debe agregar el `.env` las siguientes variables:

- `FILE_CONTENT_EXCEL`: Contenido del archivo `.xlsx` de prueba
- `FILE_CONTENT_CSV`: Contenido del archivo `.csv` de prueba
- `FILE_CONTENT_TXT`: Contenido del archivo `.txt` de prueba

Se puede ejecutar el archivo de testing:
```bash
python -m pytest database/test/test_files.py
python -m pytest database/test/test_finds.py
python -m pytest database/test/test_inserts.py
```
También se puede ejecutar una función de prueba individual:
```bash
py -m pytest database/test/test_files.py::test_read_excel
```

## Modelos
**`database/entity/node.py`**: Representa un Nodo de la red.<br>
**`database/models/node.py`**: Representa la respuesta de la base de datos para un Nodo de la red.