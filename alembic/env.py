import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.database import Base  # Import your Base

# this is the Alembic Config object
config = context.config

# Get the database URL from environment variable
LIVE_DATABASE_URL = os.getenv(
    "LIVE_DATABASE_URL", "postgresql://postgres:portfolio_db_#1016@db.xbdporhfcnajxzezzwuy.supabase.co:5432/postgres?sslmode=require")

# Override the sqlalchemy.url from alembic.ini
config.set_main_option("sqlalchemy.url", LIVE_DATABASE_URL)

# add your model's MetaData object here
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
