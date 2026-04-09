from typing import List
from app.domain.models import ProdutoRead, ProdutoCreate, ProdutoUpdate
from app.domain.exceptions import ProdutoNaoEncontradoError
from app.infra.repositories.produto_repository import RepositorioProduto

class ServicoProduto:
    def __init__(self, repositorio: RepositorioProduto):
        self.repositorio = repositorio
        
    def listar(self) -> List[ProdutoRead]:
        return self.repositorio.listar()
    
    def obter(self, produto_id: int) -> ProdutoRead:
        produto = self.repositorio.obter_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        return produto
    
    def criar(self, dto: ProdutoCreate) -> ProdutoRead:
        # Exemplo de regra de negócio, ex. verificar se nome já existe, etc, se necessário.
        return self.repositorio.criar(dto.nome, dto.preco, dto.descricao)
    
    def atualizar(self, produto_id: int, dto: ProdutoUpdate) -> ProdutoRead:
        produto_atual = self.obter(produto_id)
        
        # Patch/Merge de dados:
        novo_nome = dto.nome if dto.nome is not None else produto_atual.nome
        novo_preco = dto.preco if dto.preco is not None else produto_atual.preco
        nova_descricao = dto.descricao if dto.descricao is not None else produto_atual.descricao
        
        atualizado = self.repositorio.atualizar(produto_id, novo_nome, novo_preco, nova_descricao)
        if not atualizado:
            raise ProdutoNaoEncontradoError(produto_id)
            
        return self.obter(produto_id)
    
    def excluir(self, produto_id: int) -> None:
        # Se não existe, já levanta o erro. O Repositório também retornaria false, mas isso previne erros silenciosos em concorrências.
        self.obter(produto_id)
        
        excluido = self.repositorio.excluir(produto_id)
        if not excluido:
            raise ProdutoNaoEncontradoError(produto_id)
