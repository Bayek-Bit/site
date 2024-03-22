from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Diary"
)

app.mount('/static', StaticFiles(directory='public', html=True))

@app.get("/hello")
def hello():
    return "Hello!"