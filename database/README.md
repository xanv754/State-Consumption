# MODULE: DATABASE
> [Spanish version](./README_es.md)

This module handles the creation or updating of the network node database. A file of type `.xlsx`, `.csv` (delimited by `;`) or `.txt` (delimited by `,`) must be provided with the following data

- **Nodo:** Name of the node or name of central (mandatory)
- **Estado:** Location state of the node (mandatory)
- **Código Contable:** The accounting code associated with the Node. (Mandatory)
- **IP:** The service IP of the Node. (Optional)
- **Region:** The region of the location state of the Node. (Optional)

**Important:** The file must have a single column for each of the above data, i.e. the columns must not contain keywords (e.g. **Código**, **Estado** o **Nodo**) in the name, unless it is the exact column containing such information, as these words are used to identify the specific columns.

Example of columns in the file:

    ✅ Numero, Estado, Nombre del Nodo, IP, Otra columna sin palabra clave
    ❌ Numero del Nodo, Estado del Nodo, Nombre del Nodo del Estado, IP del Nodo, Otra columna con palabra clave

## Requirements
Existing libraries in the `requirements.txt` file of this project for easy installation.

## Environment Variables
An `.env` file must be provided with the following environment variables:

- `URI`: MongoDB server URI
- `DB`: Name of the database
- `MASTERNODO_PATH`: Path to the data file

## Usage
If you have a new `MASTERNODO` file to update the database, simply add the `database` module to the PYTHONPATH to run it:

```bash
python -m database
```

Otherwise you can run the file directly:
```bash
python database/__main__.py
```
There you will find the CLI for the module to get information about the different functions found in the module.

## Unit tests
If you want to run unit tests, you need to add the following variables to your `.env`

- `FILE_CONTENT_EXCEL`: Contents of the `.xlsx` test file.
- `FILE_CONTENT_CSV`: Contents of the test `.csv` file.
- `FILE_CONTENT_TXT`: Contents of the test `.txt` file

The test file is ready to run:
```bash
python -m pytest database/test/test_files.py
python -m pytest database/test/test_files.py
python -m pytest database/test/test_inserts.py
```
You can also run a single test function:
```bash
py -m pytest database/test/test_files.py::test_read_excel
```

## Models
**`database/entity/node.py`**: Represents a node in the network.<br>
**`database/models/node.py`**: Represents the database response for a node in the network.