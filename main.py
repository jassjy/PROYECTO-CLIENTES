from fastapi import FastAPI
from  modelos.clientes import Cliente, Clientecrear

app=FastAPI()


lista_clientes:list[Cliente] = []


#endpoint para listar todos los clientes
@app.get("/clientes", response_model=list[Cliente])
def listar_clientes():
    return lista_clientes

#endpoint para listar un solo cliente de la lista
@app.get("/clientes/{cliente_id}", response_model=Cliente)
def listar_clientes(cliente_id: int):
    #recorrer la lista clientes
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.get("id") == cliente_id:
            return obj_cliente
        

#endpoint para crear un cliente y agregar a la lista 
@app.post("/clientes", response_model=Cliente)
def crear_clientes(datos_cliente:Clientecrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    lista_clientes.append(cliente_val)
    return cliente_val