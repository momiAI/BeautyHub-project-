from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context


from src.database import Base  
from src.config import settings  
from src.models import *

from sqlalchemy.ext.asyncio import create_async_engine


config = context.config
fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций оффлайн"""
    url = settings.db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций онлайн (async engine)"""
    connectable = create_async_engine(
        settings.db_url,
        echo=False,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
