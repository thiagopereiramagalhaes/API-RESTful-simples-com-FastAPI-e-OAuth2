"""
Repositorio é a camada de acesso a dados que interage diretamente com o banco de dados. 
Ele encapsula as operações CRUD (Create, Read, Update, Delete) para a entidade Produto, 
garantindo que a lógica de acesso aos dados esteja separada da lógica de negócios e da apresentação.
Essa separação de responsabilidades torna o código mais modular, testável e fácil de manter."""

from typing import List, Optional
from models import Produto
from database import conexao_gerenciada

class RepositorioProduto:
    
    def listar(self) -> List[Produto]: #Read All
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM produtos ORDER BY id")
            return [Produto(**dict(row)) for row in cursor.fetchall()]
        
    def obter_por_id(self, produto_id: int) -> Optional[Produto]: #Read One
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            row = cursor.fetchone()
            return Produto(**dict(row)) if row else None
    
    def criar(self, nome: str, preco: float, descricao: Optional[str]) -> Produto: #Create
        with conexao_gerenciada() as con:
            cursor = con.execute("INSERT INTO produtos (nome, preco, descricao) VALUES (?, ?, ?)", (nome, preco, descricao))
            novo_id = cursor.lastrowid
            return Produto(id = novo_id, nome = nome, preco = preco, descricao = descricao) 
        
    def atualizar(self, produto_id: int, nome: str, preco: float, descricao: Optional[str]) -> Optional[Produto]: #Update
        with conexao_gerenciada() as con:
            cursor = con.execute("""
                                 UPDATE produtos
                                    SET nome = ?, preco = ?, descricao =?
                                    WHERE id = ?
                                 """, (nome, preco, descricao, produto_id))
            if cursor.rowcount == 0:
                return None
            return Produto(id = produto_id, nome = nome, preco = preco, descricao = descricao)
        
    def excluir(self, produto_id: int) -> bool: #Delete
        with conexao_gerenciada() as con:
            cursor = con.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            return cursor.rowcount > 0
        

class RepositorioUsuario:
    def obter_usuario_por_username(self, username: str) -> dict:
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        
