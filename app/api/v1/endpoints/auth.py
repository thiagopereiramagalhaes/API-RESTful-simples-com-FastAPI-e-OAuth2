from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.domain.models import Token
from app.domain.exceptions import CredenciaisInvalidasError
from app.infra.repositories.usuario_repository import RepositorioUsuario
from app.core.security import verificar_senha, criar_token_acesso, registrar_tentativa_falha, limpar_tentativas, ip_bloqueado
from app.infra.database import get_db
from app.core.rate_limit import limiter

router = APIRouter(tags=["Autenticação"])

@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    
    # 1. Verifica Brute Force Blocking
    if ip_bloqueado(ip):
        raise HTTPException(status_code=429, detail="Muitas tentativas falhas. IP bloqueado temporariamente.")

    # 2. Busca e Valida a Senha
    repositorio = RepositorioUsuario(db)
    usuario = repositorio.obter_usuario_por_username(form_data.username)
    
    if not usuario or not verificar_senha(form_data.password, usuario["hashed_password"]):
        registrar_tentativa_falha(ip) # Punição no IP
        raise CredenciaisInvalidasError()
        
    # 3. Sucesso! Limpa as tentativas se estiver tudo ok
    limpar_tentativas(ip)
        
    if usuario["username"] == "admin":
        permissoes = ["read", "write", "delete"]
    else:
        permissoes = ["read", "write"]
        
    token_acesso = criar_token_acesso(
        dados={"sub": usuario["username"], "scopes": permissoes},
        client_ip=ip
    )
    return {"access_token": token_acesso, "token_type": "bearer"}
