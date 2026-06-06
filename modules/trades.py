from datetime import datetime

from modules.database import engine


def add_trade(
    symbol,
    name,
    market,
    side,
    quantity,
    price,
    fee=0,
    stop_loss=None,
    take_profit=None
):

    symbol = symbol.upper()

    with engine.begin() as conn:

        # 新增交易記錄
        conn.exec_driver_sql(
        """
        INSERT INTO trades
        (
            date,
            symbol,
            name,
            market,
            side,
            quantity,
            price,
            fee
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?
        )
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            name,
            market,
            side,
            quantity,
            price,
            fee
        )
        )

        # 讀取現有持倉
        result = conn.exec_driver_sql(
        """
        SELECT
            quantity,
            avg_price,
            stop_loss,
            take_profit
        FROM holdings
        WHERE symbol=?
        """,
        (symbol,)
        ).fetchone()

        # ==========================
        # BUY
        # ==========================
        if side.lower() == "buy":

            if result:

                old_qty = float(result[0])
                old_avg = float(result[1])

                total_qty = old_qty + quantity

                new_avg = (
                    old_qty * old_avg +
                    quantity * price
                ) / total_qty

                conn.exec_driver_sql(
                """
                UPDATE holdings
                SET
                    quantity=?,
                    avg_price=?,
                    stop_loss=?,
                    take_profit=?
                WHERE symbol=?
                """,
                (
                    total_qty,
                    new_avg,
                    stop_loss,
                    take_profit,
                    symbol
                )
                )

            else:

                conn.exec_driver_sql(
                """
                INSERT INTO holdings
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
                    ?,?,?,?,?,?,?,?
                )
                """,
                (
                    symbol,
                    name,
                    market,
                    quantity,
                    price,
                    stop_loss,
                    take_profit
                )
                )

        # ==========================
        # SELL
        # ==========================
        else:

            if not result:
                raise Exception(
                    f"{symbol} 不存在持倉"
                )

            current_qty = float(result[0])

            if quantity > current_qty:

                raise Exception(
                    f"賣出數量超過持倉 ({current_qty})"
                )

            remaining = current_qty - quantity

            if remaining <= 0:

                conn.exec_driver_sql(
                """
                DELETE FROM holdings
                WHERE symbol=?
                """,
                (symbol,)
                )

            else:

                conn.exec_driver_sql(
                """
                UPDATE holdings
                SET quantity=?
                WHERE symbol=?
                """,
                (
                    remaining,
                    symbol
                )
                )
def get_realized_pnl():
    import pandas as pd


def get_realized_pnl():

    trades = pd.read_sql(
        "SELECT * FROM trades",
        engine
    )

    if trades.empty:
        return 0

    realized = 0

    positions = {}

    for _, t in trades.iterrows():

        sym = t["symbol"]

        if sym not in positions:

            positions[sym] = {
                "qty": 0,
                "avg": 0
            }

        p = positions[sym]

        if t["side"] == "buy":

            total_qty = p["qty"] + t["quantity"]

            p["avg"] = (
                p["qty"] * p["avg"] +
                t["quantity"] * t["price"]
            ) / total_qty

            p["qty"] = total_qty

        else:

            pnl = (
                t["price"] -
                p["avg"]
            ) * t["quantity"]

            realized += pnl

            p["qty"] -= t["quantity"]

    return realized
