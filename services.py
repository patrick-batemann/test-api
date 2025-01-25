from typing import TYPE_CHECKING
import database as _db
import models as _md
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _update_db():
    return _db.Base.metadata.create_all(bind=_db.engine)

def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_product(
    product: _schemas.CreateProduct,
    db: "Session"
) -> _schemas.Product:

    product = _md.Product(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return _schemas.Product.from_orm(product)