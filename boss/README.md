# MODULE: BOSS  
> [Spanish version](./README_es.md)

This module is responsible for generating the total number of clients and total consumption per state for ADSL and MDU equipment. It requires the BOSS report, which is a `.xlsx` file. The necessary columns of this file for the correct execution of the module are:

- **Nrpname:** Specification of the node's aggregator (Required).
- **Location:** Aggregator status of the node (Required)
- **Name Coid:** Name of the node (Required)
> **Note:** The chief report often has problems with some node names. For some nodes, the column data is shifted one column to the right. This needs to be corrected manually.
- **Cantidad:** Number of clients for the node (required).

And a file with the consumption by aggregator (BRAS. Also a `.xlsx` file). The necessary columns for the correct execution of the module are:

- **BRAS:** Name of the aggregators.
- **in:** Consumption of the aggregators.

## Requirements
Existing libraries in the `requirements.txt` file of this project for easy installation.

## Usage
The module has its own CLI commands, which can be executed from the command line:
```bash
python -m boss # Valid if the module is in PYTHONPATH.
python boss/__main__.py
```
There you will find usage information for each function of the module.

### Generate consumption by automatic status
```bash
python -m boss auto -fr <report_boss> -fc <consumption_file 
python -m boss/__main__.py auto -fr <boss_report> -fc <consumption_file> -fc <consumption_file>.
```
This command will create the `Consumption_by_State_ADSL_MDU.xlsx' file containing the consumption data by state.

If you want to get all the files generated at runtime, add the `-p` flag at the end of the command.
```bash
python -m boss auto -fr <reporte_boss> -fc <archivo_consumo> -p
python -m boss/__main__.py auto -fr <reporte_boss> -fc <archivo_consumo> -p
```

### Generate Consumption by Manual Status
```bash
python -m boss manual -fac <clientes_adsl_por_agregador> -fap <porcentage_clientes_adsl_por_agregador> -fmc <clientes_mdu_por_agregador> -fmp <porcentage_clientes_mdu_por_agregador> -fc <archivo_consumo>

python -m boss/__main__.py manual -fac <clientes_adsl_por_agregador> -fap <porcentage_clientes_adsl_por_agregador> -fmc <clientes_mdu_por_agregador> -fmp <porcentage_clientes_mdu_por_agregador> -fc <archivo_consumo>
```
This command generates the file `Consumo_por_Estado_ADSL_MDU.xlsx` with the data provided in the specified files. You should have both the total number of customers for each aggregator in each state and their percentage representation. For both ADSL and MDU installations.

For more information see the CLI of the module.