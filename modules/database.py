from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "sqlite:///database.db",
    echo=False
)

def init_db():

    holdings = """
    CREATE TABLE IF NOT EXISTS holdings(
        symbol TEXT PRIMARY KEY,
        name TEXT,
        market TEXT,
        quantity REAL,
        avg_price REAL,
        stop_loss REAL,
        take_profit REAL
    )
    """

    trades = """
    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        symbol TEXT,
        name TEXT,
        market TEXT,
        side TEXT,
        quantity REAL,
        price REAL,
        fee REAL
    )
    """

    with engine.connect() as conn:
        conn.exec_driver_sql(holdings)
        conn.exec_driver_sql(trades)

def get_holdings():
    return pd.read_sql("SELECT * FROM holdings", engine)

def get_trades():
    return pd.read_sql(
        "SELECT * FROM trades ORDER BY date DESC",
        engine
    )
