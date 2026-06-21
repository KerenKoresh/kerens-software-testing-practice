#!/usr/bin/env python3
"""Database migration / bootstrap for ToolShop.

Creates the schema (and seeds the baseline catalog if empty) on whatever database
DATABASE_URL points to — Postgres in production, SQLite locally.

Usage:
    python scripts/migrate.py            # create tables + seed if empty (idempotent)
    python scripts/migrate.py --reset    # DROP all tables, recreate, reseed
    python scripts/migrate.py --status   # just print the current state

Run it once after provisioning a fresh Postgres, or any time you want to reset.
"""
import os
import sys
import argparse

# Make the app package importable when run as `python scripts/migrate.py`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
import app as toolshop  # importing also ensures tables exist (app.init_db runs on import)


def status():
    with toolshop.SessionLocal() as s:
        total = s.scalar(select(func.count()).select_from(toolshop.Product))
        owned = s.scalar(
            select(func.count()).select_from(toolshop.Product)
            .where(toolshop.Product.edit_token_hash.is_not(None))
        )
    print(f"Database : {toolshop.engine.url.render_as_string(hide_password=True)}")
    print(f"Dialect  : {toolshop.engine.dialect.name}")
    print(f"Products : {total} total ({owned} created via API, {total - owned} baseline)")


def reset():
    print("Dropping all tables...")
    toolshop.Base.metadata.drop_all(toolshop.engine)
    print("Recreating schema and seeding...")
    toolshop.init_db()
    print("Done.")


def main():
    parser = argparse.ArgumentParser(description="ToolShop DB migration / bootstrap")
    parser.add_argument("--reset", action="store_true", help="drop everything and reseed")
    parser.add_argument("--status", action="store_true", help="print state and exit")
    args = parser.parse_args()

    if args.status:
        status()
        return

    if args.reset:
        reset()
    else:
        # Importing `app` already ran init_db(); make it explicit and idempotent.
        toolshop.init_db()
        print("Schema ensured and baseline seeded (if it was empty).")

    status()


if __name__ == "__main__":
    main()
