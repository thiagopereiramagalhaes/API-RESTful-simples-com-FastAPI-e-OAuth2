from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Produto, ProdutoCriar, ProdutoAtualizar, Token
from database import inicializar_banco
from repository import RepositorioProduto, RepositorioUsuario
from services import ServicoProduto, ErroDeNegocio
from security import oauth2_scheme, verificar_senha, criar_token_acesso, verificar_permissoes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado na inicialização do aplicativo
    inicializar_banco()
    yield
    # Código a ser executado na finalização do aplicativo (se necessário)   
    

app = FastAPI(title = "API de Produtos Autenticada",
              version = "1.0.0",
              description = "API para gerenciamento de produtos com autenticação via OAuth2",
              lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Somente estes endereços entram
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

def obter_servico_produto():
    repositorio = RepositorioProduto()
    servico = ServicoProduto(repositorio)
    return servico
        


    
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
        
    if usuario["username"] == "admin":
        permissoes = ["read", "write", "delete"]
        
    else:
        permissoes = ["read", "write"]
        
    token_acesso = criar_token_acesso(dados={"sub": usuario["username"], "scopes": permissoes})
    return {"access_token": token_acesso, "token_type": "bearer"}

    
@app.get("/", tags=["Main"])
def main():
    return {"message": "Bem-vindo à API de Produtos Autenticada! Consulte /docs para testar no Swagger"}

@app.get("/produtos", response_model=List[Produto], tags=["Produtos"])
def listar_produtos(
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.listar()

@app.get("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def obter_produto(
    produto_id: int,
    current_user: str = Security(verificar_permissoes, scopes=["read"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    try:
        return servico.obter(produto_id)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.post("/produtos", response_model=Produto, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def criar_produto(
    dto: ProdutoCriar,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    return servico.criar(dto)

@app.put("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def atualizar_produto(
    produto_id: int,
    dto: ProdutoAtualizar,
    current_user: str = Security(verificar_permissoes, scopes=["write"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    try:
        return servico.atualizar(produto_id=produto_id, dto=dto)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos"])
def excluir_produto(
    produto_id: int,
    current_user: str = Security(verificar_permissoes, scopes=["delete"]),
    servico: ServicoProduto = Depends(obter_servico_produto)
):
    try:
        servico.excluir(produto_id)
    except ErroDeNegocio as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))