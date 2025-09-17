from fastapi import FastAPI
from core.config import get_settings
from api.v1.routes.user_route import user_route
from middlewares.middleware import add_user_to_request_state
import uvicorn

settings = get_settings()

app = FastAPI(debug=settings.DEBUG)


@app.get("/")
def read_item():
    return {
        "OrcaHelper": "Ajuda a voce ver o que pode comprar da sua lista de desejos e te alerta caso a data do produto esteja perto de expirar"
    }


app.middleware("http")(add_user_to_request_state)

app.include_router(user_route, tags=["/user"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,  # só em dev! cuidado em produção
    )
