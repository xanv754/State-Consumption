# MÓDULO: BOSS
> [English version](./README.md)

Este módulo se encarga de generar el total de clientes y el total de consumo por estado para los equipos ADSL y MDU. Para ello, se debe proporcionar el reporte de BOSS, el cual es un archivo de tipo `.xlsx`. Las columnas necesarias de dicho archivo para la correcta ejecución del módulo son:

- **Nrpname:** Especificación del agregador del nodo. (Obligatorio)
- **Location:** Especificación del estado de agregador del nodo. (Obligatorio)
- **Name Coid:** Nombre del nodo. (Obligatorio)
> **Nota:** El reporte boss suele tener problemas con algunos nombres del nodo. Algunos nodos tiene los datos de la columna movidos una columna hacia la derecha. Se debe corregir manualmente.
- **Cantidad:** Cantidad de clientes del nodo. (Obligatorio)

Y un archivo con los consumos por agregador (BRAS. También de tipo `.xlsx`). La columna necesaria para la correcta ejecución del módulo son:

- **BRAS:** Nombre de los agregadores.
- **in:** Consumo de los agregadores.

## Requerimientos
Librerías existentes en el archivo `requirements.txt` de este proyecto para su fácil instalación.

## Uso
Para poder obtener el archivo de `Consumo_por_Estado_ADSL_MDU.xlsx`, se necesita el reporte de BOSS y el archivo de consumo por BRAS (Agregador).

El módulo cuenta con su CLI, que se puede ejecutar desde la línea de comandos:
```bash
python -m boss # Valido si el módulo está en PYTHONPATH.
python boss/__main__.py
```
Ahí encontrará la información de uso de cada función del módulo.

### Generar Consumo por Estado Automático
```bash
python -m boss auto -fr <reporte_boss> -fc <archivo_consumo> 
python -m boss/__main__.py auto -fr <reporte_boss> -fc <archivo_consumo>
```
Este comando generará el archivo `Consumo_por_Estado_ADSL_MDU.xlsx` con los datos de consumo por estado.

Si se desea obtener todos los archivos generados en ejecución, se debe agregar la bandera `-p` al final del comando.
```bash
python -m boss auto -fr <reporte_boss> -fc <archivo_consumo> -p
python -m boss/__main__.py auto -fr <reporte_boss> -fc <archivo_consumo> -p
```
### Generar Consumo por Estado Manual
```bash
python -m boss manual -fac <clientes_adsl_por_agregador> -fap <porcentage_clientes_adsl_por_agregador> -fmc <clientes_mdu_por_agregador> -fmp <porcentage_clientes_mdu_por_agregador> -fc <archivo_consumo>

python -m boss/__main__.py manual -fac <clientes_adsl_por_agregador> -fap <porcentage_clientes_adsl_por_agregador> -fmc <clientes_mdu_por_agregador> -fmp <porcentage_clientes_mdu_por_agregador> -fc <archivo_consumo>
```
Este comando generará el archivo `Consumo_por_Estado_ADSL_MDU.xlsx` con los datos proporcionados en los archivos indicados. Se debe tener tanto el total de clientes de cada agregador en cada estado, como su representación porcentual. Ambos para los equipos ADSL y MDU.

Para más información, consulte el CLI del módulo.

### Generar Total de Clientes por Agregador
```bash
python -m boss clients -fr <reporte_boss>
python -m boss/__main__.py clients -fr <reporte_boss>
```
Este comando generará el archivo `Clientes_por_Bras.xlsx` con el total de clientes para cada agregador.

Para más información, consulte el CLI del módulo.