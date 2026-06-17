from pydantic import BaseModel


#crear el modelo clientes (id, nombre, email, descripcion)
class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

class Clientecrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int | None = None