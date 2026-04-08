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
    
    @field_validator("nome")
    def nome_tamanho_minimo(cls, value):
        if len(value) < 3:
            raise ValueError("Nome do produto deve ter pelo menos 3 caracteres.")
        return value.strip()
    
    @field_validator("nome")
    def nome_tamanho_maximo(cls, value):
        if len(value) > 100:
            raise ValueError("Nome do produto deve ter no máximo 100 caracteres.")
        return value.strip()
    
    @field_validator("preco")
    def preco_positivo(cls, value):
        if value <= 0:
            raise ValueError("Preço do produto deve ser um valor positivo.")
        return value
    
    @field_validator("preco")
    def preco_decimais(cls, value):
        if round(value, 2) != value:
            raise ValueError("Preço do produto deve ter no máximo 2 casas decimais.")
        return value
    
    @field_validator("preco")
    def preco_limite(cls, value):
        if value > 10000:
            raise ValueError("Preço do produto deve ser menor ou igual a 10.000.")
        return value
    
    @field_validator("descricao")
    def descricao_tamanho_maximo(cls, value):
        if value and len(value) > 500:
            raise ValueError("Descrição do produto deve ter no máximo 500 caracteres.")
        return value.strip() if value else value
    
class ProdutoCriar(ProdutoBase):
    pass

class ProdutoAtualizar(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int = Field(..., example=1)
    
    
class Token(BaseModel):
    access_token: str
    token_type: str