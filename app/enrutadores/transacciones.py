from fastapi import APIRouter, HTTPException, status
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from ..listas import lista_facturas, lista_transacciones
from ..conexion_bd import sesion_dependencia
from sqlmodel import select

rutas_transacciones = APIRouter()



# 1. Listar todas las transacciones
@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def ListarTransacciones(sesion: sesion_dependencia):
    #consulta = select(Transaccion)
    #sesion.exec(consulta).all()
    #return lista_transacciones
    return sesion.exec(select(Transaccion)).all()


# 2. Obtener una sola transacción por ID
@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def ListarTransaccion(transaccion_id: int, sesion: sesion_dependencia):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)
    if not transaccion_bd:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La transacción con id {transaccion_id} no existe"
        )
    return transaccion_bd
    
   

# 3. Crear una transacción asociada a una factura 
@rutas_transacciones.post("/facturas/{factura_id}/transacciones", response_model=Transaccion)
async def CrearTransaccion(factura_id: int, datos_transaccion: TransaccionCrear, sesion: sesion_dependencia):
    factura_encontrada = None
    
    # Buscar la factura en la lista de facturas
    factura_encontrada = sesion.get(Factura, factura_id)
           
    # Validar si no existe la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La Factura con id {factura_id} no existe (Asegúrate de que ya esté creada)"
        )
    
    # Validar datos de la transacción -json y pasamos a dict
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_validada = Transaccion.model_validate(transaccion_dict)
    #guardar en bd
    sesion.add(transaccion_validada)
    sesion.commit()
    sesion.refresh(transaccion_validada)
    return transaccion_validada


# 4. Editar una transacción existente
@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EditarTransaccion(transaccion_id: int, datos_transaccion: TransaccionEditar, sesion: sesion_dependencia):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)
    if not transaccion_bd:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"La transacción con id {transaccion_id} no existe"
        )
    transaccion_dict = datos_transaccion.model_dump(exclude_unset=True)
    transaccion_bd.sqlmodel_update(transaccion_dict)
    sesion.add(transaccion_bd)
    sesion.commit()
    sesion.refresh(transaccion_bd)
    return transaccion_bd
   


# 5. Eliminar una transacción
@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EliminarTransaccion(transaccion_id: int, sesion: sesion_dependencia):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)
    if not transaccion_bd:
         raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"La transacción con id {transaccion_id} no existe"
        )
    sesion.delete(transaccion_bd)
    sesion.commit()
    return transaccion_bd
                    
       
   