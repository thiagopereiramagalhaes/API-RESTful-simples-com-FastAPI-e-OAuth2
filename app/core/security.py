from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, Request, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# --- Brute Force Protection Tracker ---
FALHAS_DE_LOGIN_POR_IP = {}
MAX_FALHAS = 5

def registrar_tentativa_falha(ip: str):
    if ip not in FALHAS_DE_LOGIN_POR_IP:
        FALHAS_DE_LOGIN_POR_IP[ip] = 0
    FALHAS_DE_LOGIN_POR_IP[ip] += 1

def limpar_tentativas(ip: str):
    if ip in FALHAS_DE_LOGIN_POR_IP:
        del FALHAS_DE_LOGIN_POR_IP[ip]

def ip_bloqueado(ip: str) -> bool:
    return FALHAS_DE_LOGIN_POR_IP.get(ip, 0) >= MAX_FALHAS

# --- Core Security ---

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SCOPES = {
    "read": "Permissão para ler dados",
    "write": "Permissão para escrever dados",
    "delete": "Permissão para deletar dados"
}

# Esquema do OAuth2
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    scopes=SCOPES
)

def verificar_senha(senha_plana, senha_com_hash):
    return pwd_context.verify(senha_plana, senha_com_hash)

def obter_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict, client_ip: str | None = None):
    dados_para_codificar = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expiracao})
    if client_ip:
        dados_para_codificar.update({"client_ip": client_ip})
    return jwt.encode(dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def verificar_permissoes(request: Request, security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        token_ip = payload.get("client_ip")
        
        # IP Binding (Opcional)
        request_ip = request.client.host if request.client else None
        if token_ip and token_ip != request_ip:
             raise HTTPException(
                status_code=403,
                detail="IP não autorizado ou alterado.",
                headers={"WWW-Authenticate": authenticate_value},
            )

        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=403,
                    detail="Não tem permissão suficiente",
                    headers={"WWW-Authenticate": authenticate_value},
                )
                
        # Injecta dinamicamente a propriedade '_current_user' originária do verify para repassar no Depends downstream.
        request.state.current_user = username
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
