# Requerimientos
## Variables de Entorno
Para poder ejecutar alguna operación con la base de datos, es necesario definir la variable de entorno `URI` con la URI de la base de datos en cualquier archivo de configuración.
- Para entorno de desarrollo: `.env.development`
- Para entorno de producción: `.env.production`
- Para entorno general: `.env`

> *Nota:* Las variables de entorno de desarrollo tiene prioridad sobre las de producción y general. Es recomendable solo definir un archivo de configuración.

# CLI
## Migraciones
Para realizar las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --migration
```

## Rollback
Para realizar el rollback de las migraciones de la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --rollback
```

## Agregar nuevo nodo
Para agregar un nuevo nodo a la base de datos, se debe ejecutar el comando:
```bash 
python main.py database --add
```
Esto solicitará al usuario que ingrese los datos del nodo que se desea agregar.
