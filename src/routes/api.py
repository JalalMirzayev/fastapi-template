from fastapi import APIRouter
from src.routes import todos
from src.routes import posts
from src.routes import users
from src.routes import auth
from src.routes import vote

router = APIRouter()
router.include_router(todos.router)
router.include_router(posts.router)
router.include_router(users.router)
router.include_router(auth.router)
router.include_router(vote.router)
