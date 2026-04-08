
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from security import obter_hash_senha
import os
from dotenv import load_dotenv

load_dotenv() 

PASSWORD_ADMIN = os.getenv("PASSWORD_ADMIN")
CAMINHO_BANCO = Path(__file__).parent / "database.db"

def obter_conexao():
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False) # Permite que o banco de dados funcione com múltiplas threads
    con.row_factory = sqlite3.Row # Permite acessar as colunas por nome em vez de por índice
    return con

@contextmanager
def conexao_gerenciada():
    con = obter_conexao()
    try:
        yield con
        con.commit()
        
    except:
        con.rollback()
        raise
    
    finally:
        con.close()
        
def inicializar_banco():
    with conexao_gerenciada() as con:
        con.execute(""" 
                    CREATE TABLE IF NOT EXISTS produtos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        preco REAL NOT NULL,
                        descricao TEXT
                    );
                    """)
        
        
        con.execute(""" 
                    CREATE TABLE IF NOT EXISTS usuarios(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        hashed_password TEXT NOT NULL
                    );
                    """)
        
        try:
            con.execute("""
                        INSERT INTO usuarios (username, hashed_password) VALUES (?, ?)
                        """, ("admin", obter_hash_senha(PASSWORD_ADMIN))
                        )
            
        except:
            pass