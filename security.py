"""
Security é um módulo que lida com a autenticação e autorização dos usuários. 
Ele inclui funções para hash de senhas, verificação de senhas e criação de tokens JWT para autenticação. 
Ele também define um esquema OAuth2 para integração com o FastAPI.
"""

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext  # noqa: F401
from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env   

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SCOPES = {
    "read": "Permissão para ler dados",
    "write": "Permissão para escrever dados",
    "delete": "Permissão para deletar dados"
}

# Esquema do OAuth2 (O FastAPI usará isso para criar o botão de Auth no Swagger)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SCOPES
    )

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

async def verificar_permissoes(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_scopes = payload.get("scopes", []) # Busca os escopos do token
        
        # Verifica se todos os escopos exigidos pela rota estão no token
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=403,
                    detail="Não tem permissão suficiente",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")