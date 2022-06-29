from fastapi import FastAPI, Depends
from src.api.views import api_router
from src.blockchain.blockchain import Blockchain


def create_app():
    app_ = FastAPI()
    app_.include_router(api_router)
    return app_


blockchain = Blockchain()
app = create_app()
