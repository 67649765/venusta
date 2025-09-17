import os
import random
from typing import Any, Dict
import psycopg
from psycopg.rows import dict_row

# Read mock mode from environment variable
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Mock data for when database is not available
MOCK_DATA = {
    "responses": 5,
    "kappa": 0.76,
    "mae": 0.4,
    "papers": 10
}

MOCK_ITEMS = [
    {"id": 1, "content": "二次函数 y=x²-2x+3 的顶点坐标是什么？", "answer": "(1,2)", "difficulty": 3},
    {"id": 2, "content": "方程 x²=4 的解是什么？", "answer": "2", "difficulty": 2}
]

def get_conn():
    try:
        conn = psycopg.connect(
            dbname=os.getenv("POSTGRES_DB","venusta"),
            user=os.getenv("POSTGRES_USER","venusta"),
            password=os.getenv("POSTGRES_PASSWORD","venusta"),
            host=os.getenv("POSTGRES_HOST","localhost"),
            port=os.getenv("POSTGRES_PORT","5432"),
            autocommit=True,
            row_factory=dict_row,
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        # Return None to indicate connection failure
        return None

def fetchall(sql: str, params: tuple = ()) -> list[Dict[str, Any]]:
    conn = get_conn()
    if conn:
        try:
            with conn, conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        except Exception as e:
            print(f"Database fetchall error: {e}")
            conn.close()
    
    # Return mock data only if MOCK_MODE is true
    if MOCK_MODE:
        if "responses" in sql and "count" in sql:
            return [{"n": MOCK_DATA["responses"]}]
        elif "items" in sql:
            return MOCK_ITEMS
        elif "dashboard" in sql or "metrics" in sql:
            return [{k: v for k, v in MOCK_DATA.items()}]
    
    return []

def execute(sql: str, params: tuple = ()) -> None:
    if not MOCK_MODE:
        conn = get_conn()
        if conn:
            try:
                with conn, conn.cursor() as cur:
                    cur.execute(sql, params)
            except Exception as e:
                print(f"Database execute error: {e}")
                conn.close()
