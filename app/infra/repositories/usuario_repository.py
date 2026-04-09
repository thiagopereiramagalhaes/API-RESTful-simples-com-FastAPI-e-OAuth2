from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.infra.models_db import UsuarioDB
from app.core.security import obter_hash_senha
from app.core.config import settings

class RepositorioUsuario:
    def __init__(self, db: Session):
        self.db = db

    def obter_usuario_por_username(self, username: str) -> dict:
        usuario = self.db.query(UsuarioDB).filter(UsuarioDB.username == username).first()
        if usuario:
            return {"username": usuario.username, "hashed_password": usuario.hashed_password}
        return None

    def inicializar_usuarios_padrao(self):
        try:
            # Verifica se já existe admin
            if not self.db.query(UsuarioDB).filter(UsuarioDB.username == "admin").first():
                admin = UsuarioDB(username="admin", hashed_password=obter_hash_senha(settings.PASSWORD_ADMIN))
                self.db.add(admin)
                
            if not self.db.query(UsuarioDB).filter(UsuarioDB.username == "usuario").first():
                usr = UsuarioDB(username="usuario", hashed_password=obter_hash_senha(settings.PASSWORD_ADMIN))
                self.db.add(usr)
                
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
