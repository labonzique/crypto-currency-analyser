binance = "https://api.binance.com/api/v3/ticker/price"
token = " "

class PostgreSqlConfig(object):
    DB_USER = " "
    DB_PASSWORD = " "
    DB_HOST = " "
    DB_NAME = " "
    DB_PORT = " "
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
