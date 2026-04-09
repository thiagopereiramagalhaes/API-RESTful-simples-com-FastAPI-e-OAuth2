class ErroDeNegocio(Exception):
    """Classe base para erros de negócio e de domínio."""
    pass

class ProdutoNaoEncontradoError(ErroDeNegocio):
    def __init__(self, produto_id: int):
        self.produto_id = produto_id
        super().__init__(f"Produto com id {produto_id} não encontrado.")

class UsuarioNaoEncontradoError(ErroDeNegocio):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Usuário {username} não encontrado.")

class CredenciaisInvalidasError(ErroDeNegocio):
    def __init__(self):
        super().__init__("Usuário ou senha inválidos.")
