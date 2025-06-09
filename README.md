# Consumo por Estado - State Consumption
Automatización en Python para procesar los datos de clientes y consumo de la red para obtener totales por estado.

Para más información sobre los archivos necesarios para el procesamiento, actualización de la base de datos, etc... Puedes consultar el [Manual](./MANUAL.md).

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
Si se presenta errores de módulos, puedes exportar el PYTHONPATH para corregir los errores de importación.
```bash
export PYTHONPATH=$(pwd)
``` 

# Interfaz de Línea de Comandos
Este módulo tiene una interfaz de línea de comandos (CLI) para poder ejecutar las operaciones.
```bash 
python main.py --help
```

Para más información sobre las operaciones disponibles, puedes consultar el [Manual](./src/state_consumption/MANUAL.md).
