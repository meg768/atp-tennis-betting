"""Optional direct MariaDB access. HTTP service clients are unaffected."""

import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import sys

from dotenv import dotenv_values
import pymysql


ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class DatabaseError(Exception):
    """A deliberately sanitized error safe to display to the user."""


def connect():
    """Connect using only the project-local .env, without environment expansion."""
    try:
        config = dotenv_values(ENV_FILE, interpolate=False)
        if any(not config.get(key) for key in
               ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")):
            raise ValueError
        port = int(config.get("DB_PORT") or "3306")
        if not 1 <= port <= 65535:
            raise ValueError
    except Exception:
        raise DatabaseError("Invalid or missing database settings in local .env.") from None
    try:
        return pymysql.connect(
            host=config["DB_HOST"], port=port, database=config["DB_NAME"],
            user=config["DB_USER"], password=config["DB_PASSWORD"],
            charset="utf8mb4", autocommit=False, connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except Exception:
        raise DatabaseError("Database connection failed; check settings and access.") from None


@contextmanager
def transaction():
    """Commit on success, roll back on failure, and always close the connection.

    MariaDB DDL can commit implicitly and cannot generally be rolled back.
    Raw driver exceptions are intentionally replaced to avoid leaking secrets.
    """
    connection = connect()
    try:
        yield connection
        connection.commit()
    except BaseException as error:
        try:
            connection.rollback()
        except Exception:
            pass
        if isinstance(error, Exception):
            raise DatabaseError("Database operation failed; details suppressed.") from None
        raise
    finally:
        try:
            connection.close()
        except Exception:
            pass


def execute(sql, params=None):
    """Execute one statement, with optional PyMySQL %s parameters.

    No SQL operation is filtered; the account's grants determine permissions.
    Returns one entry per result set, including stored procedure results.
    """
    results = []
    with transaction() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            while True:
                results.append({
                    "rows": cursor.fetchall() if cursor.description else [],
                    "rowcount": cursor.rowcount,
                })
                if not cursor.nextset():
                    break
    return results


def main():
    parser = argparse.ArgumentParser(description="Run one MariaDB SQL statement.")
    parser.add_argument("file", nargs="?", type=Path,
                        help="UTF-8 SQL file; omit to read standard input")
    args = parser.parse_args()
    try:
        sql = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        if not sql.strip():
            raise DatabaseError("SQL input is empty.")
        result = execute(sql)
    except DatabaseError as error:
        print(str(error), file=sys.stderr)
        return 1
    except Exception:
        print("Unable to read SQL input; details suppressed.", file=sys.stderr)
        return 1
    print(json.dumps(result, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
