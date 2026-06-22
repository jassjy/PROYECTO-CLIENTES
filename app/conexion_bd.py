from fastapi import FastAPI ,Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine


nombre_bd = "bd_Cliente.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#motor de bd
motor_bd = create_engine(url_bd)

#definir el metodo para crear las tablas 
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #no hay nada para retornar o ejjecutar


#definir el metodo para la sesion
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion#retorna la sesion

#Denominado inyeccion de dpendencias.
#registrar la sesion como dependencia, uttilizada en nuestros endpoints
sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]