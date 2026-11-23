import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

DATABASE_PATH = Path("site.db")


class MessageCreate(BaseModel):
    text: str


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


@app.get("/api/messages")
def get_messages():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id, text, author FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()

    connection.close()

    return [
        {"id": message[0], "text": message[1], "author": message[2]}
        for message in messages
    ]


@app.post("/api/messages", status_code=201)
def create_message(message: MessageCreate):
    text = message.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Сообщение не может быть пустым")

    if len(text) > 200:
        raise HTTPException(status_code=400, detail="Сообщение длиннее 200 символов")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO messages (text, author) VALUES (?, ?)",
        (text, "Гость"),
    )
    message_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {"id": message_id, "text": text, "author": "Гость"}


app.mount("/", StaticFiles(directory=".", html=True), name="site")
