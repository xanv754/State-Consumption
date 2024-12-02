# MODULE: OLT
> [Spanish version](./README_es.md)

This module is responsible for formatting the consumption and customer totals by OLT equipment status. It requires the OLT file, which is a file of type `.xlsx`. The columns required for the module to run correctly are

- **Estado:** Node site status (Required).
- **Usuarios:** Number of users of the node (Required)
- **Consumo:** OLT Node usage. (Required)

## Requirements
Existing libraries in the `requirements.txt` file of this project for easy installation.

## Usage
The module has its own CLI command which can be used from the command line:
```bash
python -m olt # Valid if the module is in the PYTHONPATH.
python olt/__main__.py
```
This will give you usage information for each function in the module.

### Generate usage by state
```bash
python -m olt auto -fr <olt_file>
python -m olt/__main__.py auto -fr <olt_file>
```
This command will generate the `Consumo_por_Estado_OLT.xlsx' file containing the consumption and totalisation data for customers by state.

See the module CLI for more information.