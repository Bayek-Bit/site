# Здесь будут запросы на sql

from sqlalchemy import text

from database import engine

from datetime import datetime

from collections import defaultdict



class Core:
    
    # @staticmethod
    # async def add_student():
    #     pass
    
    @staticmethod
    async def get_marks(student_id: int, week_start: datetime, week_end: datetime):
        async with engine.connect() as conn:
            # Получем id предмета(присоединяем subject), оценку, дату оценки и название предмета по id пользователя в диапазоне недели. 
            query = text("""
                        SELECT mark.subject_id, mark.mark, mark.set_date, subject.name FROM mark
                        JOIN subject ON mark.subject_id = subject.id
                        WHERE mark.student_id = :student_id
                        AND mark.set_date >= :week_start
                        AND mark.set_date <= :week_end
                     """)
            query = query.bindparams(student_id=student_id, 
                                     week_start=week_start, 
                                     week_end=week_end)
            result = await conn.execute(query)
            result = result.fetchall()
            # Создаем словарь, где ключами будут дни недели
            marks_by_day = defaultdict(list)

            # Добавляем данные в словарь, используя день недели как ключ
            for subject_id, mark, set_date, name in result:
                day_of_week = set_date.strftime("%A")  # Получаем название дня недели
                marks_by_day[day_of_week].append((name, mark))

            # Получаем словарь с днями недели, оценками за каждый день и названию предмета, по которому получена оценка
            return marks_by_day
        
        
    # @staticmethod
    # async def get_user_role(email):
    #     async with engine.connect() as conn:
    #         # Получаем роль пользователя и отдаём фронту впоследствии
    #         query = text("""SELECT role_id FROM public.user WHERE email=:email""")
    #         query = query.bindparams(email=email)
    #         user_result = await conn.execute(query)
    #         user_result = user_result.fetchone()
    #         if user_result:
    #             return user_result[0]
    #         else:pass
    #             print("No way")
    #             return None