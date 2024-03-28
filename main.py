from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Diary"
)

app.mount('/static', StaticFiles(directory="E:/www/public", html=True), name="public")

@app.get("/hello")
def hello():
    return "Hello!"