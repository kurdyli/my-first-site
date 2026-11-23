import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

DATABASE_PATH = Path("site.db")


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM messages")
    messages_count = cursor.fetchone()[0]

    if messages_count == 0:
        cursor.execute(
            "INSERT INTO messages (text, author) VALUES (?, ?)",
            ("Привет из SQLite-базы данных!", "Python + SQLite"),
        )

    connection.commit()
    connection.close()


create_database()


@app.get("/api/message")
def get_message():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT text, author FROM messages WHERE id = 1")
    message = cursor.fetchone()

    connection.close()

    return {
        "message": message[0],
        "author": message[1],
    }


app.mount("/", StaticFiles(directory=".", html=True), name="site")