from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import database, schemas, crud
from database import get_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

@app.post("/products/", response_model=schemas.ProductOut)
async def create_product(product: schemas.ProductCreate, db=Depends(database.get_db)):
    try:
        return await crud.create_product(db, product)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB Error")

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db=Depends(database.get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[schemas.ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = await crud.get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@app.put("/products/{product_id}/stock")
async def update_stock(product_id: int, delta: int, db=Depends(database.get_db)):
    try:
        product = await crud.update_stock(db, product_id, delta)
        return {"product_id": product.id, "new_quantity": product.quantity}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB Error")
