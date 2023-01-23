from fastapi import FastAPI 
import funciones_carga

app = FastAPI()

@app.get("/")
async def motor():
    print("Request recibida")
    prod= funciones_carga.motor()
    return prod





