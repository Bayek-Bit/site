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

    async def get_teacher_name_by_id(self, teacher_id):
        if self.connection:
            # Получаем список из 1 объекта (Record)
            a = await self.connection.fetch("SELECT first_name, last_name, father_name FROM teachers WHERE id = $1", teacher_id)
            
            # На выходе получаем словарь, в котором содержится имя, фамилия и отчество учителя.
            return {
                    "first_name": a[0]["first_name"],
                    "last_name": a[0]["last_name"],
                    "father_name": a[0]["father_name"]
                    }
        
    async def get_subject_by_id(self, subject_id):
        if self.connection:
            subject_name = await self.connection.fetch("SELECT name FROM subjects WHERE id = $1", subject_id)
            return subject_name[0]["name"]
            

    async def get_classes_list(self, teacher_id):
        if self.connection:
            # Получаем id классов, которые обучает учитель. Пример: [<Record class_id=1>]
            classes = await self.connection.fetch("SELECT class_id FROM teachers_users WHERE teacher_id = $1", teacher_id)
            # Создаём список, который хранит id классов, которые обучает учитель
            classes_id = []
            for i in classes:
                classes_id.append(i["class_id"])
            return classes_id
    
    async def get_students_timetable(self, student_id):
        if self.connection:
            class_id = await self.connection.fetch("SELECT class_id FROM students WHERE id = $1", student_id)
            class_id = class_id[0]["class_id"]

            # print(class_id) => 2

            timetable = await self.connection.fetch("SELECT * FROM timetable WHERE class_id = $1", class_id)

            return timetable
 

async def main():
    db = Database_worker(host=host, user=user, password=password, db_name=db_name)
    await db.connect()
    await db.get_subject_by_id(2)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
