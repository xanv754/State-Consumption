# MÓDULO: CONSUMO (MEASUREMENT)
> [English version](./README.md)

Este módulo se encarga de obtener el consumo por agregadores. Sirve para obtener el consumo de Traffic Access (Taccess) o obtener los totales de consumo de un archivo externo (dado los consumo por interfaces).

## Requerimientos
Librerías existentes en el archivo `requirements.txt` de este proyecto para su fácil instalación.

## Variables de Entorno
Se necesita proporcionar un archivo `.env` si se quiere utilizar la extracción del consumo desde la API de Taccess:

- `TACCESS_URL`: URL del servidor Taccess

## Uso
El módulo cuenta con su CLI, que se puede ejecutar desde la línea de comandos:
```bash
python -m measurement # Valido si el módulo está en PYTHONPATH.
python measurement/__main__.py
```
Ahí encontrará la información de uso de cada función del módulo.

### Consumo de Taccess
```bash
python -m measurement taccess
python measurement/__main__.py taccess
```
Este comando obtiene el consumo de Traffic Access (Taccess) y lo guarda en el archivo `consumo_taccess.xlsx`.

### Consumo de un archivo externo
```bash
python -m measurement external -f <archivo> 
python measurement/__main__.py external -f <archivo> 
```
Este comando totaliza los consumos de los agregadores de un archivo externo y lo guarda en el archivo `consumo_agregador.xlsx`. Se debe proporcionar el archivo que contenga las siguientes columnas:

- **Agregador:** Nombre de los agregadores.
- **Consumo:** Consumo de los agregadores.

Si el archivo tiene más de una hoja, se debe especificar la hoja con la que se debe trabajar `-s`.

```bash
python -m measurement external -f <archivo> -s <hoja> 
python measurement/__main__.py external -f <archivo> -s <hoja> 
```

Para más información, consulte el CLI del módulo.