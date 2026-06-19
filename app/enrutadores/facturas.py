from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura,FacturaCrear, FacturaEditar
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar
from ..listas import lista_clientes, lista_facturas
#ListaFacturas: list[Factura] = []
#ListaClientes: list[Cliente] = []

rutas_facturas = APIRouter()

#||||||||||||||||||||||||||||||||
#crear los endpoints para facturas

@rutas_facturas.get("/facturas", response_model=list[Factura])
async def lista_Facturas():
    return lista_facturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def ListaFactura(factura_id: int):
    #recorrer la lista facturas
    for  factura in enumerate(lista_facturas):
        if factura[1].id == factura_id:
            return factura[1]

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"la factura con id {factura_id}, no existe."
    )


@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    #buscar el cliente en la lista clientes
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
           cliente_encontrado = cliente
    # MENSAJE si no existe el cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cliente con id {cliente_id} no existe"
        )
    
   #validar datos de la factura
    factura_validada = Factura.model_validate(datos_factura.model_dump())
    factura_validada.cliente = cliente_encontrado
    
    #id de la factura
    factura_validada.id = len(lista_facturas) + 1
    lista_facturas.append(factura_validada)

    return factura_validada


  




@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def EditarFactura(factura_id: int, datos_factura: Factura):
    pass

@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def EliminarFactura(factura_id: int):
    # 1. Buscar la factura por su ID y obtener su posición (índice) en la lista
    for indice, factura in enumerate(lista_facturas):
        if factura.id == factura_id:
            # 2. Si la encuentra, la saca de la lista usando .pop()
            factura_eliminada = lista_facturas.pop(indice)
            # 3. Retorna la factura que se eliminó
            return factura_eliminada

    # 4. Si recorre toda la lista y no la encuentra, lanza un error 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Factura con id {factura_id} no encontrada"
        )




