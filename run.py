from app import create_app
from alembic.config import Config
from alembic import command

app = create_app()
# Run migrations

alembic_cfg = Config("../migrations/alembic.ini")  # Path to your Alembic configuration file
command.upgrade(alembic_cfg, "head")
