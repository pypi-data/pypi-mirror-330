import os

# 📌 プロジェクトのルートディレクトリ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📌 インスタンスディレクトリ（データベースの保存先）
INSTANCE_DIR = os.path.join(BASE_DIR, "instances")
os.makedirs(INSTANCE_DIR, exist_ok=True)

# 📌 使用するデータベースの種類（sqlite, mysql, postgresql）
DB_TYPE = "sqlite"

# 📌 SQLite のカスタムパス設定（None にするとデフォルトを使用）
CUSTOM_SQLITE_DB_PATH = None

# 📌 CSV ファイルの保存ディレクトリ
DEFAULT_CSV_DIR = os.path.join(BASE_DIR, "csv")
CUSTOM_CSV_DIR = None

CSV_DIR = os.path.abspath(CUSTOM_CSV_DIR) if CUSTOM_CSV_DIR else DEFAULT_CSV_DIR
os.makedirs(CSV_DIR, exist_ok=True)

# 📌 各データベースの接続設定
if DB_TYPE == "sqlite":
    if CUSTOM_SQLITE_DB_PATH:
        DB_PATH = os.path.abspath(CUSTOM_SQLITE_DB_PATH)
    else:
        DB_PATH = os.path.join(INSTANCE_DIR, "database.db")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

elif DB_TYPE == "mysql":
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = "3306"
    MYSQL_DB = "monitor_app"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

elif DB_TYPE == "postgresql":
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "password"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"
    POSTGRES_DB = "monitor_app"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

else:
    raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")

# 📌 SQLAlchemy 設定
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 📌 許可されたテーブルのみを表示
ALLOWED_TABLES = {
    "users": {"columns": ["id", "name", "email"], "primary_key": "id"},
    "products": {"columns": ["id", "name", "price"], "primary_key": "id"},
    "orders": {
        "columns": ["id", "user_id", "product_id", "amount"],
        "primary_key": "id",
        "foreign_keys": {"user_id": "users.id", "product_id": "products.id"},
        "join": """
            SELECT orders.id, users.name AS user_name, products.name AS product_name, orders.amount
            FROM orders
            JOIN users ON orders.user_id = users.id
            JOIN products ON orders.product_id = products.id
        """,
    },
}

# 📌 ヘッダーとフッターの設定
APP_TITLE = "Monitor App"
HEADER_TEXT = "📊 Monitor Dashboard"
FOOTER_TEXT = "© 2025 Monitor App - Powered by Flask & Bootstrap"
FAVICON_PATH = "favicon.ico"

# 📌 **テーブルセルのスタイル**
TABLE_CELL_STYLES = {
    "orders": {
        "amount": {
            "greater_than": {"value": 10, "class": "bg-danger text-white"},
            "less_than": {"value": 5, "class": "bg-warning text-dark"},
            "equal_to": {"value": 7, "class": "bg-success text-white"},
        }
    },
    "products": {
        "price": {
            "greater_than": {"value": 1000, "class": "bg-primary text-white"},
            "less_than": {"value": 500, "class": "bg-info text-dark"},
            "equal_to": {"value": 750, "class": "bg-secondary text-white"},
        }
    },
}
