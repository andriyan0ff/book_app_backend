from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2

class Transaction(Resource):
    def post(self):
        try:
            status = {
                "status": "created"
            }
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("new user")
            parser.add_argument("old user")
            parser.add_argument("book")
            parser.add_argument("st transaction")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO transactions (new_user, old_user, book, st_transactions)
                VALUES
                ('"""+ str(params["new user"]) +"""', '"""+ str(params["old user"]) +"""',
                '"""+ str(params["book"]) +"""', '"""+ str(params["st transaction"]) +"""');
                """)
            return  status, 200
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")