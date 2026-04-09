from typing import List, Optional
from app.domain.models import ProdutoRead
from app.infra.database import conexao_gerenciada

class RepositorioProduto:
    
    def listar(self) -> List[ProdutoRead]:
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM produtos ORDER BY id")
            return [ProdutoRead(**dict(row)) for row in cursor.fetchall()]
        
    def obter_por_id(self, produto_id: int) -> Optional[ProdutoRead]:
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            row = cursor.fetchone()
            return ProdutoRead(**dict(row)) if row else None
    
    def criar(self, nome: str, preco: float, descricao: Optional[str]) -> ProdutoRead:
        with conexao_gerenciada() as con:
            cursor = con.execute("INSERT INTO produtos (nome, preco, descricao) VALUES (?, ?, ?)", (nome, preco, descricao))
            novo_id = cursor.lastrowid
            return ProdutoRead(id=novo_id, nome=nome, preco=preco, descricao=descricao) 
        
    def atualizar(self, produto_id: int, nome: str, preco: float, descricao: Optional[str]) -> bool:
        with conexao_gerenciada() as con:
            cursor = con.execute("""
                                 UPDATE produtos
                                    SET nome = ?, preco = ?, descricao = ?
                                    WHERE id = ?
                                 """, (nome, preco, descricao, produto_id))
            return cursor.rowcount > 0
        
    def excluir(self, produto_id: int) -> bool:
        with conexao_gerenciada() as con:
            cursor = con.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            return cursor.rowcount > 0
