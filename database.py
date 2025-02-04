import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

DATABASE_URL = "postgresql://postgres:password@0.0.0.0:5432/fastapi_test"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()

Base.metadata.create_all(bind=engine) # Создание таблицы