"""Alembic environment configuration for CogniFlow."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.database import Base
from app.core.config import settings

# Import all models so SQLAlchemy metadata contains every table.
from app.models import (  # noqa: F401
    ContextSwitch,
    Developer,
    Event,
    FlowSession,
    Interruption,
    Metric,
    Task,
    Team,
    task_developers,
)


# ---------------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata used by Alembic autogenerate.
target_metadata = Base.metadata


# Use the application's DATABASE_URL instead of requiring a
# database password/URL to be hard-coded in alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)


# ---------------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------
# Online migrations
# ---------------------------------------------------------------


def do_run_migrations(connection: Connection) -> None:
    """Run migrations using an active database connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations."""

    configuration = config.get_section(
        config.config_ini_section,
    )

    if configuration is None:
        configuration = {}

    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations,
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations against the configured PostgreSQL database."""

    asyncio.run(
        run_async_migrations(),
    )


# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()