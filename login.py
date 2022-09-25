from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2

class Login(Resource):
    def post(self):
        try:
            passed = {
                "status":  "True"
            }
            filed = {
                "status": "False"
            }
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("login")
            parser.add_argument("password")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM users WHERE login = '""" + str(params["login"]) + """' 
                               and password = '""" + str(params["password"]) + """';""")
                data = cursor.fetchall()
                if len(data) != 0:
                    return passed, 200
                else:
                    return filed, 404

        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")