# Observatorio FCCA

## Observatorio de gestión pública e inteligencia de mercados

El objetivo del mismo es proporcionar a la comunidad académica de la Facultad de Contaduría y Ciencias Administrativas, de la Universidad Michoacana de San Nicolás de Hidalgo y al público en general, información confiable, sistematizada y actualizada referente a los precios de mercado de granos, frutas y hortalizas.

[La lista de productos y claves] (https://app1.observatorio-fcca-umich.com/api/get_sniim_productos)

```
from observatoriofcca import sniimapp
import pandas as pd

username = 'USUARIO'   
password = 'PASSWORD'  
limit = 50  
offset = 0  

client = sniimapp.sniimapp_precios(username=username,password=password)

prices = client.get_sniim_precios(
    product_key="FH-CD42", date_start="2024-02-01", date_end="2024-04-10"
)
```
