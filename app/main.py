from fastapi import FastAPI 
import funciones_etl
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def presentacion():
    return FileResponse("./Presentacion.md")

@app.get("/products")
async def products():
    prod= funciones_etl.products_etl()
    return prod

@app.get("/sellers")
async def sellers():
    sell= funciones_etl.sellers_etl()
    return sell

@app.get("/customers")
async def customers():
    cust= funciones_etl.customers_etl()
    return cust

@app.get("/orders")
async def orders():
    orde= funciones_etl.orders_etl()
    return orde

@app.get("/geolocation")
async def geolocation():
    geo= funciones_etl.geolocation_etl()
    return geo

@app.get("/marketing_qualified_leads")
async def marketing_qualified_leads():
    mql= funciones_etl.marketing_qualified_leads_etl()
    return mql

@app.get("/order_items")
async def order_items():
    ord_item= funciones_etl.order_items_etl()
    return ord_item

@app.get("/payments")
async def payments():
    ord_pay= funciones_etl.order_payments_etl()
    return ord_pay

@app.get("/order_reviews")
async def order_reviews():
    ord_rev= funciones_etl.order_reviews_etl()
    return ord_rev

@app.get("/closed_deals")
async def closed_deals():
    cdeals= funciones_etl.closed_deals_etl()
    return cdeals

@app.get("/zip_code_prefix")
async def zip_code_prefix():
    zcp= funciones_etl.zip_code_prefix()
    return zcp




