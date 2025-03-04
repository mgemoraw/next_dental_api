from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import auth_route
from api.routes import (
    users_route,
    patients_route,
    assets_route,
    posts_route,
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://10.161.70.69:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users_route.router)
app.include_router(auth_route.router)
app.include_router(patients_route.router)
app.include_router(assets_route.router)
app.include_router(posts_route.router)