from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from models import Product

async def create_product(db, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def get_product(db, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def get_all_products(db):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def update_stock(db, product_id: int, delta: int):
    async with db.begin():
        result = await db.execute(select(Product).where(Product.id == product_id).with_for_update())
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")
        if product.quantity + delta < 0:
            raise ValueError("Insufficient stock")
        product.quantity += delta
        await db.flush()
    return product
