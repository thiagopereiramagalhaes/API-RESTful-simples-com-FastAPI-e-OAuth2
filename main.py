from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from models import Produto, ProdutoCriar, ProdutoAtualizar, Token
from database import inicializar_banco
from repository import RepositorioProduto
from services import ServicoProduto, ErroDeNegocio
from security import oauth2_scheme, verificar_senha, criar_token_acesso

app = FastAPI(title = "API de Produtos Autenticada",
              version = "1.0.0",
              description = "API para gerenciamento de produtos com autenticação via OAuth2"
)

def obter_servico_produto():
    repositorio = RepositorioProduto()
    servico = ServicoProduto(repositorio)
    return servico

@app.on_event("startup")
async def iniciar():
    inicializar_banco()
    
@app.post("/token", response_model=Token, tags=["Autenticação"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repositorio = RepositorioUsuario()
    usuario = repositorio.obter_usuario_por_username(form_data.username)
    
    if not usuario or not verificar_senha(form_data.password, usuario["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token_acesso = criar_token_acesso(dados={"sub": usuario["username"]})
    return {"access_token": token_acesso, "token_type": "bearer"}

    
@app.get("/", tags=["Main"])
def main():
    return {"message": "Bem-vindo à API de Produtos Autenticada! Consulte /docs para testar no Swagger"}

@app.get("/produtos", response_model=List[Produto], tags=["Produtos"])
def listar_produtos(
    servico: ServicoProduto = Depends(obter_servico_produto),
    token: str = Depends(oauth2_scheme)
):
    return servico.listar()

@app.get("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def obter_produto(
    produto_id: int,
    servico: ServicoProduto = Depends(obter_servico_produto),
    token: str = Depends(oauth2_scheme)
):
    try:
        return servico.obter(produto_id)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.post("/produtos", response_model=Produto, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def criar_produto(
    dto: ProdutoCriar,
    servico: ServicoProduto = Depends(obter_servico_produto),
    token: str = Depends(oauth2_scheme)
):
    return servico.criar(dto)

@app.put("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def atualizar_produto(
    produto_id: int,
    dto: ProdutoAtualizar,
    servico: ServicoProduto = Depends(obter_servico_produto),
    token: str = Depends(oauth2_scheme)
):
    try:
        return servico.atualizar(produto_id=produto_id, dto=dto)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos"])
def excluir_produto(
    produto_id: int,
    servico: ServicoProduto = Depends(obter_servico_produto),
    token: str = Depends(oauth2_scheme)
):
    try:
        servico.excluir(produto_id)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))