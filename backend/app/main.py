from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# database
from db.db import Database_worker
from db.config import host, user, password, db_name

import asyncio

def create_fastapi_app():
    app = FastAPI(
        title="Diary"
    )

    origins = [
        "http://127.0.0.1:5500",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                    "Authorization"],
    )

# Database
# db = Database_worker(host=host, user=user, password=password, db_name=db_name)

# @app.get("/diary/{teacher_id}")
# async def get_info(teacher_id):
#     classes_list = await db.get_classes_list(teacher_id=teacher_id)
#     return {"classes_list": classes_list}

@app.get("/diary/{user_id}")
async def get_timetable(user_id: int):
    pass