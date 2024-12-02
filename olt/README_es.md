# MÓDULO: OLT
> [English version](./README.md)

Este módulo se encarga de formatear el consumo y los totales de clientes por estado de para los equipos OLT. Para ello, se debe proporcionar el archivo OLT, que es un archivo de tipo `.xlsx`. Las columnas necesarias para la correcta ejecución del módulo son:

- **Estado:** Estado de ubicación del nodo. (Obligatorio)
- **Usuarios:** Cantidad de usuarios del nodo. (Obligatorio)
- **Consumo:** Consumo de los nodos OLT. (Obligatorio)

## Requerimientos
Librerías existentes en el archivo `requirements.txt` de este proyecto para su fácil instalación.

## Uso
El módulo cuenta con su CLI, que se puede ejecutar desde la línea de comandos:
```bash
python -m olt # Valido si el módulo está en PYTHONPATH.
python olt/__main__.py
```
Ahí encontrará la información de uso de cada función del módulo.

### Generar el consumo por Estado
```bash
python -m olt auto -fr <archivo_olt>
python -m olt/__main__.py auto -fr <archivo_olt>
```
Este comando generará el archivo `Consumo_por_Estado_OLT.xlsx` con los datos de consumo y totalización de clientespor estado.

Para más información, consulte el CLI del módulo.