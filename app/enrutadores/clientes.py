from fastapi import APIRouter, HTTPException,status
from app.modelos.clientes import Cliente, Clientecrear, ClienteEditar
from ..listas import lista_clientes

#ListaClientes: list[Cliente] = []

rutas_clientes = APIRouter()

#endpoint, para obtener o listar todos los clientes

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def Listar_clientes():
    return lista_clientes

#endpoint, para obtener o listar un solo cliente de la lista

@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def ListarCliente(cliente_id: int):
    #recorrer la lista clientes
    for cliente in enumerate(lista_clientes):
        if cliente[1].id == cliente_id:
            return cliente[1]

    raise HTTPException(
        status_code=404, detail=f"Cliente con id {cliente_id} no encontrado"
    )

#endpoint, para crear un cliente, y agregar a la lista

@rutas_clientes.post("/clientes", response_model=Cliente)
async def AgregarCliente(datos_cliente: Clientecrear):

    ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
    
    #generar id
    id_cliente = len(lista_clientes) + 1
    ClienteValidado.id = id_cliente
    lista_clientes.append(ClienteValidado)

    return ClienteValidado


#endpoint, para editar un cliente, y agregar a la lista

@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def EditarCliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == cliente_id:
            #validar los datos del cliente
            ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
            ClienteValidado.id = cliente_id
            lista_clientes[i] = ClienteValidado
            return ClienteValidado

    raise HTTPException(status_code=400, detail=f"El cliente con id {cliente_id} no existe")

#endpoint, para eliminar un cliente, y agregar a la lista

@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def EliminarCliente(cliente_id: int):
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == cliente_id:
            ClienteEliminado = lista_clientes.pop(i)
            return ClienteEliminado

    raise HTTPException(status_code=400, detail=f"El cliente con id {cliente_id} no existe")