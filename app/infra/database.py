import sqlite3
from pathlib import Path
from contextlib import contextmanager

CAMINHO_BANCO = Path(__file__).parent.parent.parent / "database.db"

def obter_conexao():
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

@contextmanager
def conexao_gerenciada():
    con = obter_conexao()
    try:
        yield con
        con.commit()
    except Exception:
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
