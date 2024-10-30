# CLIENTS CONSUMPTION BY STATE
This mini-project has been created to automate the calculations to get tables with percentages of consumption by state.

## CLI
This project has its own CLI command, which can be executed from the command line:
```bash
python main.py
```

### Generate consumption by state
```bash
python main.py consumption -fr <boss_report> -fo <olt_file> -fc <consumption_file> -fc <consumption_file>
```
This command creates the `CONSUMPTION_BY_STATE_VPTI_VPTI.xlsx` file containing the consumption data by state. It requires the BOSS report, the consumption file by OLT and the consumption file by BRAS (aggregator).

For more information, refer to the CLI of the module or the documentation of each module.