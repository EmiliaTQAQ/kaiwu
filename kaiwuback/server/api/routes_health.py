"""Health-check API routes."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from server.persistence.db import get_db


REQUIRED_DB_TABLES = ("conversations", "messages", "agent_tasks", "agent_events")


def register_health_routes(app: FastAPI):
    """Register health-check endpoints that do not expose secrets."""

    @app.get("/api/health/db")
    def api_database_health():
        try:
            db = get_db()
            try:
                with db.cursor() as cur:
                    cur.execute("SELECT 1")
                    cur.execute("SELECT DATABASE()")
                    database_name = cur.fetchone()[0]
                    missing_tables: list[str] = []
                    for table_name in REQUIRED_DB_TABLES:
                        cur.execute(
                            """
                            SELECT 1
                            FROM information_schema.tables
                            WHERE table_schema = DATABASE()
                              AND table_name = %s
                            LIMIT 1
                            """,
                            (table_name,),
                        )
                        if not cur.fetchone():
                            missing_tables.append(table_name)
            finally:
                db.close()
        except Exception as exc:
            print(f"[DB_HEALTH] Database unavailable: {type(exc).__name__}", flush=True)
            return JSONResponse(
                {
                    "status": "error",
                    "database": "unavailable",
                    "error": "database connection failed",
                    "error_type": type(exc).__name__,
                },
                status_code=503,
            )

        if missing_tables:
            return JSONResponse(
                {
                    "status": "error",
                    "database": "connected",
                    "schema": "missing_tables",
                    "missing_tables": missing_tables,
                    "migration_hint": "Run `python -m alembic upgrade head` from kaiwuback/.",
                },
                status_code=503,
            )

        return {
            "status": "ok",
            "database": "connected",
            "schema": "ready",
            "database_name": database_name,
        }
