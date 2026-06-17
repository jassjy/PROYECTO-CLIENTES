from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura,FacturaCrear, FacturaEditar
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar

ListaFacturas: list[Factura] = []
ListaClientes: list[Cliente] = []

rutas_facturas = APIRouter()

#||||||||||||||||||||||||||||||||
#crear los endpoints para facturas

@rutas_facturas.get("/facturas", response_model=list[Factura])
async def ListarFacturas():
    return ListaFacturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def ListarFactura(factura_id: int):
    #recorrer la lista facturas
    for  factura in enumerate(ListaFacturas):
        if factura.id == factura_id:
            return factura

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"la factura con id {factura_id}, no existe."
    )


@rutas_facturas.post("/facturas", response_model=Factura)
async def CrearFactura(cliente_id: int, datos_factura: FacturaCrear):
    #buscar el cliente en la lista clientes
    cliente_encontrado = None
    for cliente in ListaClientes:
        if cliente.id == cliente_id:
           cliente_encontrado = cliente
    # MENSAJE si no existe el cliente
    if not cliente_encontrado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cliente con id {cliente_id} no existe")
    
    #validar datos de la factura
    factura_validada = Factura.model_validate(datos_factura.model_dump())
    factura_validada.cliente = cliente_encontrado
    
    
    #id de la factura
    factura_validada.id = len(ListaFacturas) + 1
    ListaFacturas.append(factura_validada)

    return factura_validada




@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def EditarFactura(factura_id: int, datos_factura: Factura):
    pass

@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def EliminarFactura(factura_id: int):
    pass




