from app import create_app
from alembic.config import Config
from alembic import command

app = create_app()
with app.app_context():
    # Run migrations
    alembic_cfg = Config("migrations/alembic.ini")
    command.upgrade(alembic_cfg, "head")
