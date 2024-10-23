# CLIENTS X CONSUMPTION
This project was created to automate the calculations to obtain tables with percentages of consumption by BRAS and States.

## CLI COMMANDS

### DATABASE
Update the database with nodes.
```bash
py -m database # Shows the help
py -m database update -e file # Updates the database with a external file.
py -m database update -e input # Updates the database with input data.
```

### BOSS
Create the total clients report by state and bras.
```bash
py -m boss # Shows the help.
py -m boss clients # Creates the report.
```

### MEASUREMENT
Get measurements from Taccess API.
```bash
py -m measurement # Shows the help.
py -m measurement taccess # Gets measurements from Taccess API.
```

### GLOBAL
Calculates the total consumption by bras and state.
```bash
py -m main # Shows the help.
py -m main total -p /path/the/porcentage/file.xlsx -c /path/the/consumption/file.xlsx # Creates the consumption by bras file to data ADSL and MDU.
py -m main total -o /path/the/olt/file.xlsx # Creates the consumption by bras file to data OLT.
```

## Environment Variables
This variables are to the database module.

- URI: Mongo URI
- DB: Database name

