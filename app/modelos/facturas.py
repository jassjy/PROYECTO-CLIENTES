from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from .transacciones import Transaccion
from .clientes import Cliente, ClienteLeer
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now()) 
    #cliente: Cliente
    #transacciones: list[Transaccion] = []


    @computed_field
    @property
    def vr_total(self) -> float:        
        total_factura = 0.0
        if self.transacciones== None:
            return total_factura
        #recorrer las transacciones, segun el id de la factura

        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura

class FacturaCrear(FacturaBase):
    cliente: Cliente
    transacciones: list[Transaccion] =[]


class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #crear relaciones virtuales,transacciones - NO en la bd
    transacciones: list[Transaccion] = Relationship(back_populates="factura")
    cliente: Cliente = Relationship(back_populates="facturas")

#modelo para mostrar al usurario o el cliente
class FacturaLeer(FacturaBase):
    id: int
    cliente: ClienteLeer

class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transaccion] = []
    