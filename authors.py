from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2

class Authors(Resource):
    def get(self, id):
        try:
            jsonData = []
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            if id == 0:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM authors;""")
                    data = cursor.fetchall()
                    for row in data:
                        result = {}
                        result["id"] = row[0]
                        result["name"] = row[1]
                        jsonData.append(result)
                return jsonData, 200
            if id > 0:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM authors WHERE id = '"""+str(id)+"""';""")
                    data = cursor.fetchall()
                    if len(data) != 0:
                        for row in data:
                            result = {}
                            result["id"] = row[0]
                            result["name"] = row[1]
                            jsonData.append(result)
                        return jsonData, 200
                    else:
                        return "id not found", 404
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def post(self):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("name")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM authors WHERE name = '""" + str(params["name"]) + """';""")
                data = cursor.fetchall()
                if len(data) == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO authors (name)
                            VALUES
                            ('"""+ str(params["name"]) +"""');""")
                    return "New authors created!", 201
                else:
                    return "A authors with this name already exists", 409
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
