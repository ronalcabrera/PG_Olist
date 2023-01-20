from fastapi import FastAPI 
import funciones_etl
import funciones_carga
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def motor():
    prod= funciones_carga.motor()
    return prod





