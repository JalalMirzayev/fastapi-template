```bash
python -m venv venv
cd venv/scripts && activate.bat && cd.. && cd..
python -m pip install fastapi[all]
python -m pip install passlib[bcrypt]
python -m pip install python-jose[cryptography]
python -m pip install alembic
```

# Generating Secret for JWT
Open git bash and type `openssl rand -hex 32`.

# Working with `alembic`

```bash
alembic --help
alembic init alembic
# Change target_metadata from None to Base.metadata
# > target_metadata = Base.metadata
# Open `./alembic.ini` and chane `sqlalchemy.url` = 
```

Open the file `./alembic/env.py` and add the following two imports.

```python
from src.models.votes import Base
from src.config import settings
```

Then change the `target_metadata` from `None` to `Base.metadata` and add the following lines below `config = context.config`

```python
config.set_main_option(
    'sqlalchemy.url',
    f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')
```

## Revisions with alembic
```bash
alembic revision --autogenerate -m "init"
```

