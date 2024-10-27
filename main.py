from fastapi import FastAPI
from routes import item_routes
from db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(item_routes.router)