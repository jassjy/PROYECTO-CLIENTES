from fastapi import APIRouter, HTTPException,status
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar
from ..listas import lista_clientes
from ..conexion_bd import sesion_dependencia
from sqlmodel import select, Session

#ListaClientes: list[Cliente] = []

rutas_clientes = APIRouter()

#endpoint, para obtener o listar todos los clientes

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def Listar_clientes(sesion: sesion_dependencia):
    lista_cli = sesion.exec(select(Cliente)).all()
    return lista_cli

#endpoint, para obtener o listar un solo cliente de la lista

@rutas_clientes.get(
    "/clientes/{cliente_id}",
      response_model=Cliente
)
async def ListarCliente(cliente_id: int, mi_sesion: sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {cliente_id} no encontrado"
        )
    return cliente_bd
    
  
  

#endpoint, para crear un cliente, y agregar a la lista

@rutas_clientes.post("/clientes", response_model=Cliente)
async def AgregarCliente(datos_cliente: Clientecrear, mi_sesion: sesion_dependencia):

    ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
    
    mi_sesion.add(ClienteValidado)
    mi_sesion.commit()
    mi_sesion.refresh(ClienteValidado)    
    return ClienteValidado


#endpoint, para editar un cliente, y agregar a la lista

@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def EditarCliente(cliente_id: int, datos_cliente: ClienteEditar, mi_sesion: sesion_dependencia
):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {cliente_id} no encontrado"
        )
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return cliente_bd

#endpoint, para eliminar un cliente, y agregar a la lista

@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def EliminarCliente(cliente_id: int, mi_sesion: sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {cliente_id} no encontrado"
        )
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    return cliente_bd
   