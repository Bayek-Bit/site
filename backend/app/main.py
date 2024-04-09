# TODO: auth and login 

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# database
from db.queries.orm import AsyncORM



async def main():
    await AsyncORM.create_tables()
    await AsyncORM.select_teachers()




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


    @app.get("/diary/{user_id}")
    async def get_timetable(user_id: int):
        pass

    return app

app = create_fastapi_app()  

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="main:app",
        reload=True
    )