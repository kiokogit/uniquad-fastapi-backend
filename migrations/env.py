from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from core.settings import settings
from database.connection import Base

# import models so Alembic sees them
from acl.models import *
from posts.models import *

config = context.config

def include_object(object, name, type_, reflected, compare_to):
    # Only include tables that are present in Base.metadata.tables, i.e., our models imported above
    if type_ == "table":
        # Ensure only tables from Base.metadata (i.e., our own models) are included
        return name in Base.metadata.tables
    return False


# 🔑 OVERRIDE the URL properly
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
