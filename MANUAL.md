# Tabla de Contenido
- [Requerimientos](#requerimientos)
- [Interfaz de Línea de Comandos](#interfaz-de-línea-de-comandos)
- [Archivos Para Procesar](#archivos-para-procesar)
    - [BOSS](#boss)
    - [ASF](#asf)
    - [BRAS](#bras)
- [Base de Datos](#base-de-datos)
    - [Inicialización](#inicialización)
    - [Destrucción](#destrucción)
- [Inspección de Archivos](#inspección-de-archivos)
    - [Verificación de BOSS](#verificación-de-boss)
    - [Verificación de ASF](#verificación-de-asf)
    - [Verificación de BRAS](#verificación-de-bras)
- [Procesamiento](#procesamiento)
    - [Opciones](#opciones)
    - [Consumo por Estado General](#consumo-por-estado-general)

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
python -m state_consumption --help
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
- HOSTNAME: Nombre del nodo.
- ESTADO: Estado del nodo.

## BRAS
El archivo BRAS (agregador) es un archivo en excel que contiene la información del consumo de los agregadores en la red.

Este archivo no es necesario que contenga algún nombre de columna en específico. Sin embargo, es necesario que la primera columna estén los nombres de los agregadores y en la segunda columna estén los consumos de los agregadores.

El archivo puede estar totalizado globalmente por agregador o tener el consumo a detalle por agregador. Si es este último caso, es necesario colocar la bandera `--process` al final del comando para procesamiento de datos.

# Base de Datos
Este proyecto trabaja con una base de datos para el almacenamiento de la información de los nodos de la red, esto con el fin de poder tener un registro de los nodos con sus estados y otros datos necesarios para el procesamiento.

## Inicialización
Para realizar el inicio correcto de la base de datos, se debe ejecutar el comando:
```bash 
python -m state_consumption.database --start
```

## Destrucción
Para realizar la destrucción de la base de datos, se debe ejecutar el comando:
```bash 
python -m state_consumption.database --destroy
```

# Inspección de Archivos
Existe un comando para inspeccionar los archivos BOSS, ASF y BRAS. Esto con el fin de verificar que los archivos están correctamente formateados antes de realizar el verdadero procesamiento. Este comando solo verifica que los datos estén en el formato correcto y no realiza ningún procesamiento. Para ejecutar el comando, se debe ejecutar el siguiente comando:

## Verificación de BOSS
```bash 
python -m state_consumption inspect --boss <ruta del archivo BOSS>
```

## Verificación de ASF
```bash 
python -m state_consumption inspect --asf <ruta del archivo ASF>
```

## Verificación de BRAS
```bash 
python -m state_consumption inspect --bras <ruta del archivo BRAS>
```
> *Nota:* Si el archivo de consumo por bras no está totalizado globalmente por agregador, se debe ejecutar el comando con el parámetro `--process`. Si no se realiza esta operación, es posible que ocurra un error o no se obtenga correctamente la información.
```bash 
python -m state_consumption inspect --bras <ruta del archivo BRAS> --process
```

# Procesamiento

### Opciones
#### `--process`
Si el archivo de consumo por bras no está totalizado globalmente por agregador, se debe ejecutar el comando con el parámetro `--process`. Si no se realiza esta operación, es posible que ocurra un error o no se obtenga correctamente la información.

*Ejemplo:*
```bash 
python -m state_consumption vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras> --process
```

#### `--filepath`
Por defecto, los archivos procesados se exportarán en el directorio *Descargas* (O *Downloads*) con un nombre por defecto. Si se desea cambiar el nombre del archivo, se debe especificar toda la ruta del archivo en la opción `--filepath`.

*Ejemplo:*
```bash 
python -m state_consumption vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras> --filepath <ruta del archivo>
```

#### `--percentage`
Si se desea obtener los porcentajes de consumo, se debe especificar la opción `--percentage`.

*Ejemplo:*
```bash 
python -m state_consumption vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras> --percentage
```

> *Nota:* Todas estas opciones se aplican a los comandos de procesamiento de los datos.

## Consumo por Estado General
Para ejecutar el procesamiento y obtención de consumo por estado de ADSL, MDU y OLT, se debe ejecutar el comando:
```bash 
python -m state_consumption vpti --boss <ruta del archivo BOSS> --asf <ruta del archivo ASF> --bras <ruta del archivo de consumo por bras>
```

## Consumo Totalizado por Bras
Para ejecutar el procesamiento y obtención de consumo totalizado por bras, se debe ejecutar el comando:
```bash 
python -m state_consumption bras --filepath <ruta del archivo de consumo por bras>
```