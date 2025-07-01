from utils.library.libs import mysql
from data.config import *

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host=HOST.split(':')[0],
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE_SELECT,
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci"
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS warn_staff (
                staffer VARCHAR(255) NOT NULL,
                warn INT DEFAULT 0,
                max_warns INT DEFAULT {MAX_WARNS},
                PRIMARY KEY (staffer)
            );
        """)
        conn.commit()
        return conn
    except mysql.connector.Error as err:
        print(f"Errore nella connessione al database: {err}")
        return None
