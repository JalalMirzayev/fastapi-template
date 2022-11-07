from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.todo import TodoReturn
from src.schemas.todo import TodoBase
from src.models import todo

# The following lines are handled by alembic
# from src.models.database import engine
# todo.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found"}}
)


@router.get('/', response_model=list[TodoReturn])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(todo.Todo).all()
    return todos


@router.get('/{id}', response_model=TodoReturn)
def get_todo(id: int, db: Session = Depends(get_db)):
    current_todo = db.query(todo.Todo).where(todo.Todo.id == id).first()
    if current_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no item with id={id}.')
    return current_todo


@router.post('/', response_model=TodoReturn, status_code=status.HTTP_201_CREATED)
def create_todo(body: TodoBase, db: Session = Depends(get_db)):
    todo_new = todo.Todo(description=body.description, completed=body.completed)
    db.add(todo_new)
    db.commit()
    return todo_new


@router.put('/{id}', response_model=TodoReturn)
def update_todo(id: int, body: TodoBase, db: Session = Depends(get_db)):
    todo_current = db.query(todo.Todo).filter(todo.Todo.id == id).first()
    if todo_current is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no item with id={id}.'
        )
    todo_current.description = body.description
    todo_current.completed = body.completed
    db.commit()
    return todo_current


@router.delete("/{id}", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
def delete_todo(id: int, db: Session = Depends(get_db)):
    db.query(todo.Todo).where(todo.Todo.id == id).delete()
    db.commit()
    return {'message': f'Todo with id={id} was deleted.'}
