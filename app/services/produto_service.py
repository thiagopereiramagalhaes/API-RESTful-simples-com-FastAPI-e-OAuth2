from typing import List
from app.domain.models import ProdutoRead, ProdutoCreate, ProdutoUpdate
from app.domain.exceptions import ProdutoNaoEncontradoError
from app.infra.repositories.produto_repository import RepositorioProduto
from app.core.logger import registrar_auditoria

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
    
    def criar(self, dto: ProdutoCreate, user: str, ip: str) -> ProdutoRead:
        novo_produto = self.repositorio.criar(dto.nome, dto.preco, dto.descricao)
        registrar_auditoria(user, ip, "CRIAR", "Produto", "SUCESSO", f"Produto_id: {novo_produto.id}, Nome: {novo_produto.nome}")
        return novo_produto
    
    def atualizar(self, produto_id: int, dto: ProdutoUpdate, user: str, ip: str) -> ProdutoRead:
        produto_atual = self.obter(produto_id)
        
        novo_nome = dto.nome if dto.nome is not None else produto_atual.nome
        novo_preco = dto.preco if dto.preco is not None else produto_atual.preco
        nova_descricao = dto.descricao if dto.descricao is not None else produto_atual.descricao
        
        atualizado = self.repositorio.atualizar(produto_id, novo_nome, novo_preco, nova_descricao)
        if not atualizado:
            registrar_auditoria(user, ip, "ATUALIZAR", "Produto", "FALHA", f"Produto {produto_id} não encontrado após validação prévia.")
            raise ProdutoNaoEncontradoError(produto_id)
            
        registrar_auditoria(user, ip, "ATUALIZAR", "Produto", "SUCESSO", f"Produto_id: {produto_id} modificado.")
        return self.obter(produto_id)
    
    def excluir(self, produto_id: int, user: str, ip: str) -> None:
        self.obter(produto_id)
        
        excluido = self.repositorio.excluir(produto_id)
        if not excluido:
            registrar_auditoria(user, ip, "EXCLUIR", "Produto", "FALHA", f"Produto {produto_id} falhou na exclusão.")
            raise ProdutoNaoEncontradoError(produto_id)
            
        registrar_auditoria(user, ip, "EXCLUIR", "Produto", "SUCESSO", f"Produto_id: {produto_id} removido.")
