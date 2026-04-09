from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models import ProdutoRead
from app.infra.models_db import ProdutoDB

class RepositorioProduto:
    def __init__(self, db: Session):
        self.db = db
    
    def listar(self) -> List[ProdutoRead]:
        resultados = self.db.query(ProdutoDB).all()
        return [ProdutoRead.model_validate(p) for p in resultados]
        
    def obter_por_id(self, produto_id: int) -> Optional[ProdutoRead]:
        produto = self.db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
        if produto:
            return ProdutoRead.model_validate(produto)
        return None
    
    def criar(self, nome: str, preco: float, descricao: Optional[str]) -> ProdutoRead:
        novo_produto = ProdutoDB(nome=nome, preco=preco, descricao=descricao)
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return ProdutoRead.model_validate(novo_produto)
        
    def atualizar(self, produto_id: int, nome: str, preco: float, descricao: Optional[str]) -> bool:
        produto = self.db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
        if produto:
            produto.nome = nome
            produto.preco = preco
            produto.descricao = descricao
            self.db.commit()
            return True
        return False
        
    def excluir(self, produto_id: int) -> bool:
        produto = self.db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
        if produto:
            self.db.delete(produto)
            self.db.commit()
            return True
        return False
