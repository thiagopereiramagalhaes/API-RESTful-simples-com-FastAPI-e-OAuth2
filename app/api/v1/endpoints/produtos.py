from fastapi import APIRouter, Depends, Security, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.domain.models import ProdutoRead, ProdutoCreate, ProdutoUpdate
from app.services.produto_service import ServicoProduto
from app.infra.repositories.produto_repository import RepositorioProduto
from app.core.security import verificar_permissoes
from app.infra.database import get_db
from app.core.rate_limit import limiter

router = APIRouter(prefix="/produtos", tags=["Produtos"])

def obter_servico_produto(db: Session = Depends(get_db)):
    repositorio = RepositorioProduto(db)
    return ServicoProduto(repositorio)

@router.get("/", response_model=List[ProdutoRead])
@limiter.limit("100/minute")
def listar_produtos(
    request: Request,
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.listar()

@router.get("/{produto_id}", response_model=ProdutoRead)
def obter_produto(
    produto_id: int,
    request: Request,
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.obter(produto_id)

@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(
    dto: ProdutoCreate,
    request: Request,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    ip = request.client.host if request.client else None
    return servico.criar(dto, current_user, ip)

@router.patch("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(
    produto_id: int,
    dto: ProdutoUpdate,
    request: Request,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    ip = request.client.host if request.client else None
    return servico.atualizar(produto_id, dto, current_user, ip)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(
    produto_id: int,
    request: Request,
    current_user: str = Security(verificar_permissoes, scopes=["delete"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    ip = request.client.host if request.client else None
    servico.excluir(produto_id, current_user, ip)
