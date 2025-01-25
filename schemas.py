import datetime as _dt
import pydantic as _pd

class _BaseProduct(_pd.BaseModel):
    name: str
    description: str
    price: float
    currency: str
    category: str

class Product(_BaseProduct):
    id: int
    created_at: _dt.datetime
    updated_at: _dt.datetime

class CreateProduct(_BaseProduct):
    pass

