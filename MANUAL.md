# Tabla de Contenido
- [Requerimientos](#requerimientos)
- [Interfaz de Línea de Comandos](#interfaz-de-línea-de-comandos)
- [Archivos Para Procesar](#archivos-para-procesar)
    - [BOSS](#boss)
    - [ASF](#asf)
    - [BRAS](#bras)
- [Base de Datos](#base-de-datos)
    - [Migraciones](#migraciones)
    - [Rollback](#rollback)
    - [Agregar nuevo nodo](#agregar-nuevo-nodo)
    - [Agregar/Actualizar varios nodos](#agregaractualizar-varios-nodos)
- [Procesamiento](#procesamiento)
    - [Consumo por Estado General](#consumo-por-estado-general)
    - [Consumo por Estado de ADSL](#consumo-por-estado-de-adsl)
    - [Consumo por Estado de MDU](#consumo-por-estado-de-mdu)
    - [Consumo por Estado de OLT](#consumo-por-estado-de-olt)

----------------------

# Requerimientos
## Librerías
Este proyecto contiene un archivo `requirements.txt` con las librerías necesarias para el funcionamiento del proyecto.

## Variables de Entorno
Para poder ejecutar operaciones con la base de datos, es necesario definir la variable de entorno `URI` con la URI de la base de datos en cualquier archivo de configuración.
- Para entorno de desarrollo: `.env.development`
- Para entorno de producción: `.env.production`
- Para entorno general: `.env`

> *Nota:* Las variables de entorno de desarrollo tiene prioridad sobre las de producción y general. Es recomendable solo definir un archivo de configuración.

## Exportación en el PYTHONPATH
Es recomendable exportar el PYTHONPATH para corregir los errores de importación.
```bash
export PYTHONPATH=$(pwd)
``` 

# Interfaz de Línea de Comandos
Este módulo tiene una interfaz de línea de comandos (CLI) para poder ejecutar las operaciones.
```bash 
python main.py --help
```

# Archivos Para Procesar
## BOSS
El archivo BOSS es un archivo en excel que contiene la información de los nodos de la red.

Es necesario que este archivo contenga las siguiente columnas:
- Nrpname: Parte del nombre del bras.
- Location: Parte del nombre del bras.
- Provider.1: Modelos del nodo.
- Name Coid: Nombre del nodo.
- Coid: Código contable del nodo.
- Cantidad: Cantidad de clientes del nodo.

A este archivo se le agregará la columna "Estado" que se utilizará para el procesamiento de los datos por estado. Sin embargo, el archivo puede contener una columna llamada "Estado". Si se encuentra, se utilizará esa columna para el procesamiento de los datos por estado.

## ASF
El archivo ASF es un archivo en excel que contiene la información de los nodos de la red.

Es necesario que este archivo contenga las siguiente columnas:
- DNI: Documento nacional de identidad.
- HOSTNAME: Nombre del nodo.
- ESTADO: Estado del nodo.

## BRAS
El archivo BRAS (agregador) es un archivo en excel que contiene la información del consumo de los agregadores en la red.

Este archivo no es necesario que contenga algún nombre de columna en específico. Sin embargo, es necesario que la primera columna estén los nombres de los agregadores y en la segunda columna estén los consumos de los agregadores.

El archivo puede estar totalizado globalmente por agregador o tener el consumo a detalle por agregador. Si es este último caso, es necesario colocar la bandera `--process` al final del comando para procesamiento de datos.

# Base de Datos
Este proyecto trabaja con una base de datos para el almacenamiento de la información de los nodos de la red, esto con el fin de poder tener un registro de los nodos con sus estados y otros datos necesarios para el procesamiento.

## Migraciones
Para realizar las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --migration
```

## Rollback
Para realizar el rollback de las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --rollback
```

## Agregar nuevo nodo
Para agregar un nuevo nodo a la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --add
```
Esto solicitará al usuario que ingrese los datos del nodo que se desea agregar.

## Agregar/Actualizar varios nodos
Para agregar nodos en masa es necesario tener un archivo (CSV o XLSX) con los datos de los nodos. 

El archivo debe las siguientes informaciones:
- **Estado del nodo:** El archivo debe tener una columna donde especifique el estado de cada registro. La columna puede llamarse: *Estado*, *State*. 
> *Nota:* No es importante si el nombre de la columna está en mayúsculas o minúsculas o intercalado. Tampoco es importante si el nombre de la columna contiene o no acentos.
* **Nombre del nodo:** El archivo debe tener una columna donde especifique el nombre de cada registro. La columna puede llamarse: *Central*, *Nodo*, *Centrales*, *Nodos*, *Node*, *Nodes*, *Name Coid*.
> *Nota:* No es importante si el nombre de la columna está en mayúsculas o minúsculas o intercalado. Tampoco es importante si el nombre de la columna contiene o no acentos.
* **Código contable del nodo:** El archivo debe tener una columna donde especifique el código contable de cada registro. La columna puede llamarse: *CC*, *Codigo Contable*, *Codigo_Contable*, *Account Code*, *Account_Code*.
> *Nota:* No es importante si el nombre de la columna está en mayúsculas o minúsculas o intercalado. Tampoco es importante si el nombre de la columna contiene o no acentos.

**IMPORTANTE:** **Es necesario que las columnas previamente especificadas sean únicas, ya que el sistema tomará la primera que encuentre para procesar.**

Opcionalmente, el sistema almacena la IP y la región de cada nodo. Si es posible proporcionar dicha información, los nombres de las columnas obligatoriamente deben ser: *IP*, *Region*.
> *Nota:* No es importante si el nombre de la columna está en mayúsculas o minúsculas o intercalado. Tampoco es importante si el nombre de la columna contiene o no acentos.

```bash 
python main.py update --filepath <ruta del archivo>
```

> *Nota:* Si el archivo para actualizar la base de datos es un archivo CSV, se debe especificar el parámetro `--delimiter` con el delimitador del archivo. Por defecto, el delimitador es `;`.

# Procesamiento
**IMPORTANTE:** Si el archivo de consumo por bras no está totalizado globalmente por agregador, se debe ejecutar el comando con el parámetro `--process`. Si no se realiza esta operación, es posible que ocurra un error o no se obtenga correctamente la información.

*Ejemplo:*
```bash 
python main.py vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras> --process
```

**Nota:** Por defecto, los archivos procesados se exportarán en el directorio *Descargas* (O *Downloads*) con un nombre por defecto. Si se desea cambiar el nombre del archivo, se debe especificar toda la ruta del archivo en la opción `--filepath`.

**Nota:** Si se desea obtener los porcentajes de consumo, se debe especificar la opción `--percentage`.

*Ejemplo:*
```bash 
python main.py vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras> --filepath <ruta del archivo>
```

Todas estas consideraciones se aplican a los comandos de procesamiento de los datos.

## Consumo por Estado General
Para ejecutar el procesamiento y obtención de consumo por estado de ADSL, MDU y OLT, se debe ejecutar el comando:
```bash 
python main.py vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras>
```

## Consumo por Estado de ADSL
Para ejecutar el procesamiento y obtención de consumo por estado únicamente de ADSL, se debe ejecutar el comando:
```bash 
python main.py adsl --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras>
```

## Consumo por Estado de MDU
Para ejecutar el procesamiento y obtención de consumo por estado únicamente de MDU, se debe ejecutar el comando:
```bash 
python main.py mdu --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras>
```

## Consumo por Estado de OLT
Para ejecutar el procesamiento y obtención de consumo por estado únicamente de OLT, se debe ejecutar el comando:
```bash 
python main.py olt --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras>
```

## Consumo Totalizado por Bras
Para ejecutar el procesamiento y obtención de consumo totalizado por bras, se debe ejecutar el comando:
```bash 
python main.py bras --filepath <ruta del archivo de consumo por bras>
```