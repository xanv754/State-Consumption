# CONSUMO DE CLIENTES POR ESTADO
Este mini proyecto fue creado para automatizar las cálculos para obtener tablas con porcentajes de consumo por estado.

## CLI
Este proyecto cuenta con su CLi, que se puede ejecutar desde la línea de comandos:
```bash
python main.py
```

### Generar Consumo por Estado
```bash
python main.py consumption -fr <reporte_boss> -fo <archivo_olt> -fc <archivo_consumo>
```
Este comando generará el archivo `CONSUMO_POR_ESTADO_VPTI.xlsx` con los datos de consumo por estado. Para ello se debe proporcionar el reporte de BOSS, el archivo de consumo por OLT y el archivo de consumo por BRAS (Agregador).

Para más información, consulte el CLI del módulo o la documentación de cada módulo.

