from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import api


app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)

@app.get('/')
def index():
    return {'message': 'Hello World!'}
