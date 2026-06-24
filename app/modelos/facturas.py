from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from .transacciones import Transaccion
from .clientes import Cliente
from datetime import datetime

class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now()) 
    #cliente: Cliente
    #transacciones: list[Transaccion] = []


    @computed_field
    @property
    def vr_total(self) -> float:
        #calcular(cantidad * vr_unitario)
        #consultar el id actual de la factura

        #factura_id_actual = getattr(self, "id", None)
        #total_factura = 0.0

        #if not factura_id_actual or not self.transacciones:
          #  return total_factura
        #recorrer las transacciones, segun el id de la factura

        #for transaccion in self.transacciones:
          #  if transaccion.factura_id == factura_id_actual:
             #  total_factura += transaccion.vr_unitario * transaccion.cantidad

        return 0.0

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")