# test_connection.py

from sqlalchemy import create_engine
print("gegeg")
engine = create_engine("mysql+pymysql://root:1234@localhost:3306/lifeup_db")

try:
    with engine.connect() as conn:
        print("✅ DB 연결 성공!")
except Exception as e:
    print("❌ DB 연결 실패:", e)
