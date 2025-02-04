from typing import TYPE_CHECKING, List

from fastapi import HTTPException
import database as _db
import models as _md
import schemas as _schemas
import datetime as _dt
import requests

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _update_db():        
    _db.Base.metadata.create_all(bind=_db.engine)

def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def convert(price, currency): # Функция для конвертации валют
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()
    usd_rate = data['Valute']['USD']['Value']

    match currency.upper():
        case "USD":
            price = int(price / usd_rate)
            pass
        case "RUB":
            price = int(price * usd_rate)
            pass

    return price

async def create_product(
    product: _schemas.CreateProduct,
    db: "Session"
) -> _schemas.Product:

    product = _md.Product(**product.model_dump())
    db.add(product)
        
    db.commit()
    db.refresh(product)
    return _schemas.Product.model_validate(product)


async def get_all_products(skip: int, limit: int, db: "Session") -> List[_schemas.Product]:
    total = db.query(_md.Product).count()  # Получение общего количества записей
    if skip >= total:
        raise HTTPException(status_code=404, detail="Не найдено. Попробуйте указать страницу меньше")  # Исключение, если страница слишком большая

    products = db.query(_md.Product).offset(skip).limit(limit).all()
    return list(map(_schemas.Product.model_validate, products))


async def get_product(product_id: int, db: "Session"):
    product = db.query(_md.Product).filter(_md.Product.id == product_id).first()
    return product


async def delete_product(product: _md.Product, db: "Session"):
    db.delete(product)
    db.commit()


async def update_product(
    product_data: _schemas.CreateProduct, Product: _md.Product, db: "Session"
) -> _schemas.Product:
    Product.name = product_data.name
    Product.description = product_data.description
    Product.price = product_data.price
    Product.currency = product_data.currency
    Product.category = product_data.category
    Product.updated_at = _dt.datetime.now(_dt.timezone.utc)

    db.commit()
    db.refresh(Product)

    return _schemas.Product.model_validate(Product)