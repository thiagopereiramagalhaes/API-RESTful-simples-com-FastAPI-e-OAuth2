""""
Esse modulo define os modelos de dados para a aplicação, utilizando a biblioteca Pydantic para validação e estruturação dos dados. 
Ele inclui o modelo base para produtos, que pode ser estendido para criar modelos específicos de criação e atualização de produtos.
O modelo ProductBase define os campos comuns para um produto, como nome, descrição, preço e quantidade em estoque.
Um modelo funciona como um contrato de dados, garantindo que as informações recebidas e enviadas pela API estejam no formato correto e sejam validadas antes de serem processadas.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProdutoBase(BaseModel):
    #... (Ellipsis): Indica que o campo é obrigatório
    #example: Define o valor que aparecerá automaticamente como exemplo no Swagger (/docs).
    nome: str = Field(..., example="Mouse sem fio")
    preco: float = Field(..., example=99.90)
    descricao: Optional[str] = Field(None, example="Um mouse sem fio com alta precisão.")
    
    @field_validator("nome")
    def nome_nao_vazio(cls, value):
        if not value or not value.strip():
            raise ValueError("Nome do produto não pode ser vazio.")
        return value.strip()
    
class ProdutoCriar(ProdutoBase):
    pass

class ProdutoAtualizar(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int = Field(..., example=1)
    
    
class Token(BaseModel):
    access_token: str
    token_type: str