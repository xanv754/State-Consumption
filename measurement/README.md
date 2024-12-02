# MODULE: MEASUREMENT
> [Spanish version](./README_es.md)

This module is responsible for obtaining consumption from aggregators. It is used to obtain the consumption of Traffic Access (Taccess) or to obtain the consumption totals of an external file (given the consumption by interfaces).

## Requirements
Existing libraries in the `requirements.txt` file of this project for easy installation.

## Environment Variables
You need to provide an `.env` file if you want to use consumption extraction from the Access API:

- `TACCESS_URL`: URL of the Taccess server

## Usage
The module has its own CLI, which can be used from the command line:
```bash
python -m measurement # Valid if the module is in PYTHONPATH.
python measurement/__main__.py
```
There you will find usage information for each function of the module.

### Taccess Consumption
```bash
python -m measurement taccess
python measurement/__main__.py taccess
```
This command gets the traffic access consumption and saves it to the file `consumo_taccess.xlsx`.

### Consuming an external file
```bash
python -m measure external -f <file> 
python measurement/__main__.py external -f <file>
```
This command sums the aggregator consumption from an external file and saves it to the file `consumo_agregador.xlsx`. The file must contain the following columns

- **Agregador:** Name of the aggregator.
- **Consumo:** Consumption of the aggregators.

If the file has more than one sheet, the sheet to work with `-s` must be specified.

```bash
python -m measurement external -f <file> -s <sheetname>
python measurement/__main__.py external -f <file> -s <sheetname> 
```

See the module CLI for more information.