from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import models, database, routes

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(routes.router)
