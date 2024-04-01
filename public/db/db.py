import asyncpg
from config import host, user, password, db_name

class Database_worker:
    def __init__(self, host, user, password, db_name) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
    
    async def connect(self):
        try:
            # Connect to database
            self.connection = await asyncpg.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        except Exception as _ex:
            print(f"[INFO] Error with connection to PG: {_ex}")
            self.connection = None
    
    async def check_version(self):
        if self.connection:
            version = await self.connection.fetchval("SELECT version();")
            print(f"Server version: {version}")
        else:
            print("No connection available.")

    async def get_classes_list(self, teacher_id):
        if self.connection:
            # Получаем id классов, которые обучает учитель. Пример: [<Record class_id=1>]
            classes = await self.connection.fetch("SELECT class_id FROM teachers_users WHERE teacher_id = $1", teacher_id)
            # Создаём список, который хранит id классов, которые обучает учитель
            classes_id = []
            for i in classes:
                classes_id.append(i["class_id"])
            return classes_id


async def main():
    db = Database_worker(host=host, user=user, password=password, db_name=db_name)
    await db.connect()
    await db.get_classes_list(teacher_id=1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
