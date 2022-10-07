from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2

class Transaction(Resource):
    def post(self):
        try:
            statusOk = {
                "status": "create"
            }
            statusNo = {
                "status": "error"
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
            if params["new user"] != params["old user"]:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                   SELECT login FROM users WHERE id = '"""+ str(params["new user"]) +"""'
                                   """)
                    newUser = cursor.fetchall()
                    cursor.execute("""
                                   SELECT login FROM users WHERE id = '""" + str(params["old user"]) + """'
                                   """)
                    oldUser = cursor.fetchall()
                    cursor.execute("""
                                   INSERT INTO transactions (new_user, old_user, book, st_transactions)
                                   VALUES
                                   ('"""+ str(newUser[0][0]) +"""', '"""+ str(oldUser[0][0]) +"""',
                                   '"""+ str(params["book"]) +"""', '"""+ str(params["st transaction"]) +"""');
                                   """)
                    cursor.execute("""
                                   UPDATE library SET users = '"""+ str(params["new user"]) +"""',
                                   status = 1 WHERE users = '""" + str(params["old user"]) + """'
                                   """)
                return statusOk, 200
            else:
                return statusNo, 400
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")