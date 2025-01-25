from typing import TYPE_CHECKING, List
import fastapi as _fa
import schemas as _schemas
import sqlalchemy.orm as _orm
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fa.FastAPI()

@app.post("/api/v1/products/", response_model=_schemas.Product)
async def create_product(
    product: _schemas.CreateProduct,
    db: _orm.Session = _fa.Depends(_services.get_db)
):
    return await _services.create_product(product=product, db=db)

