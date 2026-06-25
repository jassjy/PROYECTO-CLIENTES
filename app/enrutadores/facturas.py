from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura,FacturaCrear, FacturaEditar, FacturaLeer, FacturaLeerCompuesta
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar
from ..listas import lista_clientes, lista_facturas
from ..conexion_bd import sesion_dependencia
from sqlmodel import select
#ListaFacturas: list[Factura] = []
#ListaClientes: list[Cliente] = []

rutas_facturas = APIRouter()



@rutas_facturas.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def lista_Facturas(sesion: sesion_dependencia): 
    #select * from facturas
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def ListaFactura(factura_id: int, sesion: sesion_dependencia):
    factura_encontrada = sesion.get(Factura, factura_id)
    #recorrer la lista facturas
    
    if not factura_encontrada:
         raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"la factura con id {factura_id}, no existe."
    )

    return factura_encontrada

@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion: sesion_dependencia):
    #buscar el cliente en bd
    
    cliente_encontrado = sesion.get(Cliente, cliente_id)
    # MENSAJE si no existe el cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cliente con id {cliente_id} no existe"
        )
    
   #validar datos de la factura-json, pasar dict
    factura_dict = datos_factura.model_dump()
    factura_dict ["cliente_id"] = cliente_id
    factura_validada = Factura.model_validate(factura_dict)
    factura_validada.cliente = cliente_encontrado
    #guardar en bd
    sesion.add(factura_validada)
    sesion.commit()
    sesion.refresh(factura_validada)

    return factura_validada


  




@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def EditarFactura(factura_id: int, datos_factura: FacturaEditar, sesion: sesion_dependencia):
    factura_bd = sesion.get(Factura, factura_id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Factura con id{factura_id} no encontrada"
        )
    datos_enviados = datos_factura.model_dump(exclude_unset=True)
    for llave, valor in datos_enviados.items():
        if llave != "vr_total":
            setattr(factura_bd, llave, valor)
         
    sesion.add(factura_bd)
    sesion.commit()
    sesion.refresh(factura_bd)
    return factura_bd


@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def EliminarFactura(factura_id: int, sesion: sesion_dependencia):
    factura_borrar = sesion.get(Factura, factura_id)

    if not factura_borrar:
         # 4. Si recorre toda la lista y no la encuentra, lanza un error 404
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Factura con id {factura_id} no encontrada"
        )
    sesion.delete(factura_borrar)
    sesion.commit()

    return factura_borrar


   




