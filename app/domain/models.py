"""
Esse módulo define os modelos de domínio para a aplicação usando Pydantic v2.
Mantemos as regras de interface neles (tipagem e tamanho maximo) e delegamos regras complexas aos Services.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, json_schema_extra={"example": "Mouse sem fio"})
    preco: float = Field(..., gt=0, le=10000, json_schema_extra={"example": 99.90})
    descricao: Optional[str] = Field(None, max_length=500, json_schema_extra={"example": "Um mouse sem fio com alta precisão."})

    model_config = ConfigDict(from_attributes=True)

class ProdutoCreate(ProdutoBase):
    """Modelo para criar novos produtos."""
    pass

class ProdutoUpdate(BaseModel):
    """Modelo para atualizar produtos."""
    nome: Optional[str] = Field(None, min_length=3, max_length=100, json_schema_extra={"example": "Mouse Bluetooth"})
    preco: Optional[float] = Field(None, gt=0, le=10000, json_schema_extra={"example": 109.90})
    descricao: Optional[str] = Field(None, max_length=500, json_schema_extra={"example": "Versão atualizada."})
    
    model_config = ConfigDict(from_attributes=True)

class ProdutoRead(ProdutoBase):
    """Modelo para ler produtos do banco."""
    id: int = Field(..., json_schema_extra={"example": 1})

class Token(BaseModel):
    """Modelo de Token de Autenticação."""
    access_token: str
    token_type: str
