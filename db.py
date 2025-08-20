
# db.py
import sqlalchemy

def get_connection():
    username = "3apgoBueVQUtjtu.root"
    password = "ktqY75VjoaqDNsu3"
    host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
    database = "harvard_artifacts"

    conn_str = (
        f"mysql+pymysql://{username}:{password}@{host}:4000/{database}"
        "?ssl_verify_cert=false&ssl_verify_identity=false"
    )
    engine = sqlalchemy.create_engine(conn_str)
    return engine

if __name__ == "__main__":
    try:
        engine = get_connection()
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        print("✅ Database connection established successfully!")
    except Exception as e:
        print("❌ Connection failed:", e)
