# Consumo por Estado - State Consumption
Un módulo de Python para procesar los datos de clientes y consumo de la red para obtener totales por estado.

----------------------

# Requerimientos
## Variables de Entorno
Para poder ejecutar alguna operación con la base de datos, es necesario definir la variable de entorno `URI` con la URI de la base de datos en cualquier archivo de configuración.
- Para entorno de desarrollo: `.env.development`
- Para entorno de producción: `.env.production`
- Para entorno general: `.env`

> *Nota:* Las variables de entorno de desarrollo tiene prioridad sobre las de producción y general. Es recomendable solo definir un archivo de configuración.

# Interfaz de Línea de Comandos - CLI
Este módulo tiene una interfaz de línea de comandos (CLI) para poder ejecutar las operaciones de manera más sencilla.

## Problemas de  Instalación
Si se produce error al reconocer los módulos, puedes ejecutar dentro de la raíz del proyecto:
```bash
export PYTHONPATH=$(pwd)
``` 
para corregir el error.

## Consumo por Estado
Para ejecutar el procesamiento y obtención de consumo por estado, se debe ejecutar el comando:
```bash 
python main.py process --boss <ruta del archivo BOSS> --bras <ruta del archivo de consumo por bras>
```
**IMPORTANTE:** Si el archivo de consumo por bras no está totalizado globalmente por agregador, se debe ejecutar el comando con el parámetro `--process`. Si no se realiza esta operación, es posible que ocurra un error o no se obtenga correctamente la información.
```bash 
python main.py process --boss <ruta del archivo BOSS> --bras <ruta del archivo de consumo por bras> --process
```

## Database
Este módulo trabaja una base de datos para el almacenamiento de la información de los nodos de la red, esto con el fin de poder tener un registro de nodos con sus estados y otros datos necesarios para el procesamiento.

### Migraciones
Para realizar las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --migration
```

### Rollback
Para realizar el rollback de las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --rollback
```

### Agregar nuevo nodo
Para agregar un nuevo nodo a la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --add
```
Esto solicitará al usuario que ingrese los datos del nodo que se desea agregar.