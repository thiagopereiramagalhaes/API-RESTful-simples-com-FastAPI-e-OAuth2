from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.models import Token
from app.domain.exceptions import CredenciaisInvalidasError
from app.infra.repositories.usuario_repository import RepositorioUsuario
from app.core.security import verificar_senha, criar_token_acesso

router = APIRouter(tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    repositorio = RepositorioUsuario()
    usuario = repositorio.obter_usuario_por_username(form_data.username)
    
    if not usuario or not verificar_senha(form_data.password, usuario["hashed_password"]):
        raise CredenciaisInvalidasError()
        
    if usuario["username"] == "admin":
        permissoes = ["read", "write", "delete"]
    else:
        permissoes = ["read", "write"]
        
    client_ip = request.client.host if request.client else None
        
    token_acesso = criar_token_acesso(
        dados={"sub": usuario["username"], "scopes": permissoes},
        client_ip=client_ip
    )
    return {"access_token": token_acesso, "token_type": "bearer"}
