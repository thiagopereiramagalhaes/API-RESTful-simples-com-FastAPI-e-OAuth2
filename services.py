"""
Os serviços são responsáveis por conter a lógica de negócio da aplicação. 
Eles atuam como uma camada intermediária entre os controladores (endpoints) 
e os repositórios (acesso a dados).
A ideia é que os serviços sejam responsáveis por orquestrar as operações,
validar regras de negócio, e garantir a integridade dos dados.
"""

from typing import List
from models import Produto, ProdutoCriar, ProdutoAtualizar
from repository import RepositorioProduto

class ErroDeNegocio(Exception):
    """Erros de domínio"""
    
class ServicoProduto:
    def __init__(self, repositorio: RepositorioProduto):
        self.repositorio = repositorio
        
    def listar(self) -> List[Produto]:
        return self.repositorio.listar()
    
    def obter(self, produto_id: int) -> Produto:
        produto = self.repositorio.obter_por_id(produto_id)
        if not produto:
            raise ErroDeNegocio(f"Produto com id {produto_id} não encontrado.")
        return produto
    
    def criar(self, dto: ProdutoCriar) -> Produto:
        return self.repositorio.criar(dto.nome, dto.preco, dto.descricao)
    
    def atualizar(self, produto_id: int, dto: ProdutoAtualizar) -> Produto:
        atualizado = self.repositorio.atualizar(produto_id, dto.nome, dto.preco, dto.descricao)
        if not atualizado:
            raise ErroDeNegocio(f"Produto com id {produto_id} não encontrado para atualização.")
        return atualizado
    
    def excluir(self, produto_id: int) -> None:
        excluido = self.repositorio.excluir(produto_id)
        if not excluido:
            raise ErroDeNegocio(f"Produto com id {produto_id} não encontrado para exclusão.")