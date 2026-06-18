from fastapi import FastAPI, HTTPException, status
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transaccion,TransaccionCrear, TransaccionEditar
from app.enrutadores import clientes, facturas, transacciones
from app.enrutadores.clientes import rutas_clientes
from app.enrutadores.facturas import rutas_facturas
from app.enrutadores.transacciones import rutas_transacciones
from app.listas import lista_clientes, lista_facturas, lista_transacciones

app = FastAPI()


#incluir rutas de clientes
app.include_router(clientes.rutas_clientes, tags=["Clientes"])
app.include_router(facturas.rutas_facturas, tags=["Facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])
