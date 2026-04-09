import logging
import os
from datetime import datetime

# Criar e configurar logger de Auditoria
logger_auditoria = logging.getLogger("api_auditoria")
logger_auditoria.setLevel(logging.INFO)

caminho_log = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "api.log")
handler = logging.FileHandler(caminho_log, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

if not logger_auditoria.handlers:
    logger_auditoria.addHandler(handler)

def registrar_auditoria(user: str, ip: str, operacao: str, entidade: str, resultado: str, detalhes: str = ""):
    """Registra uma operação crítica. 'Quem', 'O quê', 'Resultado'."""
    ip_label = ip if ip else "IP Desconhecido"
    msg = f"Quem: {user} ({ip_label}) | O quê: {operacao} {entidade} | Resultado: {resultado} | Detalhes: {detalhes}"
    logger_auditoria.info(msg)
