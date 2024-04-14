# Здесь будут запросы на sql

from sqlalchemy import text

from db.database import engine

# class Core:
#     @staticmethod
#     async def get_student_name(email):
#         async with engine.connect() as conn:
#             # Получаем роль пользователя и отдаём фронту впоследствии
#             query = text("""SELECT role_id FROM public.user WHERE email=:email""")
#             query = query.bindparams(email=email)
#             user_result = await conn.execute(query)
#             user_result = user_result.fetchone()
#             if user_result:
#                 return user_result[0]
#             else:
#                 print("No way")
#                 return None