from fastapi import APIRouter, HTTPException, status
from app.modelos.transacciones import Transaccion,TransaccionCrear, TransaccionEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar

ListaTransacciones: list[Transaccion] = []
ListaFacturas: list[Factura] = []

rutas_transacciones = APIRouter()

#||||||||||||||||||||||||||||||||
#crear los endpoints para trasacciones

@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def ListarTransacciones():
    return ListaTransacciones

@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def ListarTransaccion(transaccion_id: int):
    pass



@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def CrearTransaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    #buscar una transaccion en la lista transacciones
    transaccion_encontrada = None
    for factura in ListaFacturas:
        if factura.id == factura_id:
           factura_encontrada = factura
    #MENSAJE si no existe la factura
    if not factura_encontrada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La Factura con id {factura_id} no existe")
    
    #validar datos de la trasaccion
    transaccion_validada = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_validada.factura_id = factura_id
    factura_encontrada.transacciones.append(transaccion_validada)
    
    #id de la trasaccion
    transaccion_validada.id = len(ListaTransacciones) + 1
    return transaccion_validada
    # falto agregar a la lista de transacciones
    ListaTransacciones.append(transaccion_validada)
    return transaccion_validada



@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EditarTransaccion(transaccion_id: int, datos_transaccion: Transaccion):
    pass

@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EliminarTransaccion(transaccion_id: int):
    pass