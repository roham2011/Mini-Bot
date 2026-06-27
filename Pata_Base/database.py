import sqlite3

db = sqlite3.connect(
    "RAG.db",
    check_same_thread=False
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
""")
db.commit() 

def reports(user_id: int, text: str):
    """Handle user reports."""
    print(f"Report from {user_id}: {text}")

    cursor.execute("""
    INSERT INTO reports(user_id , text)
    VALUES (?,?)                
    """,(user_id,text))

    db.commit()

def get_reports(user_id: int):

    cursor.execute(
        """
        SELECT *
        FROM reports
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    print (rows)

    return rows

