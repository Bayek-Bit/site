import psycopg2
from config import host, user, password, db_name

class Database_worker:
    def __init__(self) -> None:
        try:
            # Connect to database
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        except Exception as _ex:
            print(f"[INFO] Error with connection to PG: {_ex}")
            self.connection = None
        finally:
            pass

    def check_version(self):
        if self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )

                print(f"Server version: {cursor.fetchone()[0]}")
        else:
            print("No connection available.")

    def load_table(self):
        pass

if __name__ == "__main__":
    db = Database_worker()
    db.check_version()
