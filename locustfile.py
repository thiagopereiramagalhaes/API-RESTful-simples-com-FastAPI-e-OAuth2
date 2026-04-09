from locust import HttpUser, task, between
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD_ADMIN = os.getenv("PASSWORD_ADMIN")

class UsuarioAPI(HttpUser):
    # Simula um tempo de espera entre 1 e 5 segundos entre cada ação
    wait_time = between(1, 5)

    def on_start(self):
        """Executado quando um usuário virtual 'nasce'"""
        self.login()

    def login(self):
        # Substitua pelas credenciais que você criou no banco
        response = self.client.post("/api/v1/token", data={
            "username": "admin",
            "password": PASSWORD_ADMIN
        })
        if response.status_code == 200:
            token = response.json()["access_token"]
            # Define o header de autorização para as próximas requisições deste usuário
            self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(3) # Peso 3: esta tarefa será executada com mais frequência
    def listar_produtos(self):
        self.client.get("/api/v1/produtos")

    @task(1) # Peso 1: tarefa menos frequente
    def ver_raiz(self):
        self.client.get("/")