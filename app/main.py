from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.endpoints import produtos, auth
from app.infra.database import engine, Base, SessionLocal
from app.infra.repositories.usuario_repository import RepositorioUsuario
from app.domain.exceptions import ErroDeNegocio
from app.core.config import settings
from app.core.middlewares import SecurityHeadersMiddleware
from app.core.rate_limit import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa banco de dados com SQLAlchemy
    Base.metadata.create_all(bind=engine)
    
    # Inicializar usuários padrão usando SQLAlchemy Session
    db = SessionLocal()
    try:
        repo_usuario = RepositorioUsuario(db)
        repo_usuario.inicializar_usuarios_padrao()
    finally:
        db.close()
        
    yield

app = FastAPI(
    title="API de Produtos Autenticada (Clean Arch + SQLAlchemy + Advanced Security)",
    version="3.0.0",
    description="API para produtos robusta, mitigando slow brute force e aplicando boas praticas ORM",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)
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
        status_code=400, 
        content={"detail": str(exc)},
    )
    
# Tratamento de Integridade Global SQLAlchemy (Unique fields, etc)
@app.exception_handler(IntegrityError)
async def integrity_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Erro de integridade de Banco de Dados. Geralmente conflito ou violação de Unique."},
    )

@app.get("/", tags=["Main"])
def main():
    return {"message": "Bem-vindo à API de Produtos (V3)! Consulte /docs para testar no Swagger"}
