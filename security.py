"""
Security é um módulo que lida com a autenticação e autorização dos usuários. 
Ele inclui funções para hash de senhas, verificação de senhas e criação de tokens JWT para autenticação. 
Ele também define um esquema OAuth2 para integração com o FastAPI.
"""

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext  # noqa: F401

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env   

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema do OAuth2 (O FastAPI usará isso para criar o botão de Auth no Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verificar_senha(senha_plana, senha_com_hash):
    # Função para verificar a senha
    return pwd_context.verify(senha_plana, senha_com_hash)

def obter_hash_senha(senha):
    # Função para obter o hash da senha
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict):
    # Função para criar o token de acesso
    dados_para_codificar = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expiracao})
    return jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)