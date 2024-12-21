from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import users
from api.auth import auth_route
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users.router)
app.include_router(auth_route.router)
