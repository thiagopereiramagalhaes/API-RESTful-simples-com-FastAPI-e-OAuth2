from fastapi import APIRouter, Depends, Security, status
from typing import List
from app.domain.models import ProdutoRead, ProdutoCreate, ProdutoUpdate
from app.services.produto_service import ServicoProduto
from app.infra.repositories.produto_repository import RepositorioProduto
from app.core.security import verificar_permissoes

router = APIRouter(prefix="/produtos", tags=["Produtos"])

def obter_servico_produto():
    # Dependency Injection
    repositorio = RepositorioProduto()
    return ServicoProduto(repositorio)

@router.get("/", response_model=List[ProdutoRead])
def listar_produtos(
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.listar()

@router.get("/{produto_id}", response_model=ProdutoRead)
def obter_produto(
    produto_id: int,
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.obter(produto_id)

@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(
    dto: ProdutoCreate,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.criar(dto)

@router.patch("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(
    produto_id: int,
    dto: ProdutoUpdate,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.atualizar(produto_id=produto_id, dto=dto)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(
    produto_id: int,
    current_user: str = Security(verificar_permissoes, scopes=["delete"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    servico.excluir(produto_id)
