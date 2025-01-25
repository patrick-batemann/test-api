import datetime as _dt
import sqlalchemy as _sql
import database as _database

class Marketplace(_database.Base):
    __tablename__ = "Marketplace"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True, unique=True)
    description = _sql.Column(_sql.String, nullable=True)
    price = _sql.Column(_sql.Float, nullable=True)
    currency = _sql.Column(_sql.String(3))
    category = _sql.Column(_sql.String)
    created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    updated_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)