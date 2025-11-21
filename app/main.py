from fastapi import FastAPI

from app.routers.auth.login import router as auth_login_router
from app.routers.auth.me import router as auth_me_router
from app.routers.auth.register import router as auth_register_router

app = FastAPI(
    title="API de Controle Financeiro Pessoal",
    version="0.1.0",
)


app.include_router(auth_register_router)
app.include_router(auth_login_router)
app.include_router(auth_me_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Endpoint simples para verificar se a API está de pé.
    Retorna um JSON com status 'ok'.
    """
    return {"status": "OK"}
