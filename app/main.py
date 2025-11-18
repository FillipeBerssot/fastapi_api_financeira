from fastapi import FastAPI
from app.core.database import get_db

app = FastAPI(
    title="API de Controle Financeiro Pessoal",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """
    Endpoint simples para verificar se a API está de pé.
    Retorna um JSON com status 'ok'.
    """
    return {"status": "OK"}
