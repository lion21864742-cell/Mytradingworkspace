import yfinance as yf

def get_price(symbol, market):

    try:

        if market == "HK":

            code = symbol.zfill(4) + ".HK"

        else:

            code = symbol

        ticker = yf.Ticker(code)

        info = ticker.history(period="1d")

        if len(info) == 0:
            return None

        return float(info["Close"].iloc[-1])

    except:

        return None
