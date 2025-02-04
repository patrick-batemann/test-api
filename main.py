from typing import List
import fastapi as _fa
from fastapi import HTTPException, Query
import schemas as _schemas
import sqlalchemy.orm as _orm
import services as _services

app = _fa.FastAPI()

@app.post("/api/v1/products/", response_model=_schemas.Product)
async def create_product(
    product: _schemas.CreateProduct,
    db: _orm.Session = _fa.Depends(_services.get_db)
):
    if product.currency.upper() not in {"USD", "RUB"}: #Проверка введенной валюты
        raise HTTPException( 
            status_code=400,
            detail="Недопустимое значение для валюты (usd или rub)"
        )
    if product.currency.upper() == "USD": # Перевод в рубли, если валюта была указана в долларах
        new_price = await _services.convert(price=product.price, currency="RUB")
        product.price = new_price
    
    product.currency = "RUB"

    return await _services.create_product(product=product, db=db)

@app.get("/api/v1/products/", response_model=List[_schemas.Product])
async def get_product(db: _orm.Session = _fa.Depends(_services.get_db), skip: int = Query(0, ge=0, alias="page"),  # Номер страницы (по умолчанию 0)
    limit: int = Query(10, le=100)):
    return await _services.get_all_products(db=db, skip=skip, limit=limit)

@app.get("/api/v1/products/{product_id}/", response_model=_schemas.Product)
async def get_product(
    product_id: int, product_currency: str, db: _orm.Session = _fa.Depends(_services.get_db)
):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fa.HTTPException(status_code=404, detail="Продукт не найден")


    if product_currency.upper() == "USD": # Если в запросе был указан доллар, то происходит конвертация
        new_price = await _services.convert(price=product.price, currency="USD")
        product.price = new_price

    return product


@app.delete("/api/v1/products/{product_id}/")
async def delete_product(
    product_id: int, db: _orm.Session = _fa.Depends(_services.get_db)
):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fa.HTTPException(status_code=404, detail="Продукт не найден")

    await _services.delete_product(product, db=db)

    return "Удалено успешно."


@app.put("/api/products/{product_id}/", response_model=_schemas.Product)
async def update_product(
    product_id: int,
    product_data: _schemas.CreateProduct,
    db: _orm.Session = _fa.Depends(_services.get_db),
):
    product = await _services.get_product(db=db, product_id=product_id)
    if product is None:
        raise _fa.HTTPException(status_code=404, detail="Продукт не найден")
    
    if product_data.currency.upper() not in {"USD", "RUB"}: #Проверка введенной валюты
        raise HTTPException( 
            status_code=400,
            detail="Недопустимое значение для валюты (usd или rub)"
        )
    if product_data.currency.upper() == "USD": # Перевод в рубли, если валюта была указана в долларах
        new_price = await _services.convert(price=product_data.price, currency="RUB")
        product_data.price = new_price

    product_data.currency = "RUB"

    return await _services.update_product(
        product_data=product_data, Product=product, db=db
    )