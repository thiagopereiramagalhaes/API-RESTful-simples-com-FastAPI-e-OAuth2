from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.endpoints import produtos, auth
from app.infra.database import inicializar_banco
from app.infra.repositories.usuario_repository import RepositorioUsuario
from app.domain.exceptions import ErroDeNegocio
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa banco de dados e usuários padrão
    inicializar_banco()
    repo_usuario = RepositorioUsuario()
    repo_usuario.inicializar_usuarios_padrao()
    yield

app = FastAPI(
    title="API de Produtos Autenticada (Clean Architecture)",
    version="2.0.0",
    description="API para gerenciamento de produtos refinada sob Clean Architecture e OAuth2",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(auth.router, prefix="/api/v1")
app.include_router(produtos.router, prefix="/api/v1")

# Exception Handler Global para Erros de Negócio/Domínio
@app.exception_handler(ErroDeNegocio)
async def erro_de_negocio_handler(request: Request, exc: ErroDeNegocio):
    if exc.__class__.__name__ == "CredenciaisInvalidasError":
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif exc.__class__.__name__ == "ProdutoNaoEncontradoError":
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
        
    return JSONResponse(
        status_code=400, # Para regras de negócio padrão
        content={"detail": str(exc)},
    )
    
@app.get("/", tags=["Main"])
def main():
    return {"message": "Bem-vindo à API de Produtos (V2 - Clean Architecture)! Consulte /docs para testar no Swagger"}
