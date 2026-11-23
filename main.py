from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/message")
def get_message():
    return {
        "message": "Привет от Python-бэкенда!",
        "author": "FastAPI",
    }


app.mount("/", StaticFiles(directory=".", html=True), name="site")