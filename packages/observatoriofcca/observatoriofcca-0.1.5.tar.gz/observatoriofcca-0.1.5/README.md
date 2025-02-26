# Observatorio FCCA

## Observatorio de gestión pública e inteligencia de mercados

El objetivo del mismo es proporcionar a la comunidad académica de la Facultad de Contaduría y Ciencias Administrativas, de la Universidad Michoacana de San Nicolás de Hidalgo y al público en general, información confiable, sistematizada y actualizada referente a los precios de mercado de granos, frutas y hortalizas.

```
from observatoriofcca import sniimapp
import pandas as pd

username = 'USUARIO'   # solicitar usuario al responsable del proyecto
password = 'PASSWORD'  # solicitar password al responsable del proyecto
base_url = 'https://app1.observatorio-fcca-umich.com'
db_name = 'psql_1'
limit = 50  # Es la cantidad de registros que desea recibir
offset = 0  # Especifica el punto de inicio de la recuperación de datos

client = sniimapp.sniimapp_precios(username=username,password=password,base_url=base_url, db_name=db_name)

# La lista de productos y sus claves las puede consultar en https://app1.observatorio-fcca-umich.com/api/get_sniim_productos
prices = client.get_sniim_precios(
    product_key="FH-CD42", date_start="2024-02-01", date_end="2024-04-10"
)
```
