from modules.database import engine

def add_position(
    symbol,
    name,
    market,
    qty,
    avg_price,
    sl,
    tp
):

    with engine.begin() as conn:

        conn.exec_driver_sql(
        """
        INSERT OR REPLACE INTO holdings
        (
            symbol,
            name,
            market,
            quantity,
            avg_price,
            stop_loss,
            take_profit
        )
        VALUES
        (
            ?,?,?,?,?,?,?
        )
        """,
        (
            symbol,
            name,
            market,
            qty,
            avg_price,
            sl,
            tp
        )
    )

def delete_position(symbol):

    with engine.begin() as conn:

        conn.exec_driver_sql(
            "DELETE FROM holdings WHERE symbol=?",
            (symbol,)
        )
