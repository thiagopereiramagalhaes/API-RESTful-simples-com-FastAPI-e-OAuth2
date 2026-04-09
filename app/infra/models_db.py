from sqlalchemy import Column, Integer, String, Float
from app.infra.database import Base

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
