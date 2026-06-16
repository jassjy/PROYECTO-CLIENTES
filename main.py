from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def inico():
    return{"mensaje":"Hola estoy aprendiendo"}