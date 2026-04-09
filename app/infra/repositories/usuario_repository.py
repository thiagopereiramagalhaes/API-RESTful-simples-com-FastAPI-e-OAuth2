from app.infra.database import conexao_gerenciada
from app.core.security import obter_hash_senha
from app.core.config import settings
import sqlite3

class RepositorioUsuario:
    def obter_usuario_por_username(self, username: str) -> dict:
        with conexao_gerenciada() as con:
            cursor = con.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def inicializar_usuarios_padrao(self):
        with conexao_gerenciada() as con:
            try:  
                con.execute("""
                                INSERT INTO usuarios (username, hashed_password) VALUES (?, ?)
                                """, ("admin", obter_hash_senha(settings.PASSWORD_ADMIN))
                                )
                    
                con.execute("""
                                INSERT INTO usuarios (username, hashed_password) VALUES (?, ?)
                                """, ("usuario", obter_hash_senha(settings.PASSWORD_ADMIN))
                                )
            except sqlite3.IntegrityError:
                # Usuário já existe, ignoramos o erro
                pass
