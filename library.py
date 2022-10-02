from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2

class Library(Resource):
    def post(self):
        try:
            jsonData = []
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("visible")
            parser.add_argument("user")
            parser.add_argument("book")
            params = parser.parse_args()
            if str(params["visible"]) == "all" and str(params["user"]) == "" and str(params["book"]) == "":
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM status;""")
                    data = cursor.fetchall()
                    for row in data:
                        result = {}
                        result["id"] = row[0]
                        result["book"] = row[1]
                        result["user"] = row[2]
                        result["status"] = row[3]
                        jsonData.append(result)
                return jsonData, 200
            else:
                    return "sorry", 400
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")