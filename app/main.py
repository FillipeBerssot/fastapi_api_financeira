from fastapi import FastAPI

from app.routers import auth

app = FastAPI(
    title="API de Controle Financeiro Pessoal",
    version="0.1.0",
)


app.include_router(auth.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Endpoint simples para verificar se a API está de pé.
    Retorna um JSON com status 'ok'.
    """
    return {"status": "OK"}
