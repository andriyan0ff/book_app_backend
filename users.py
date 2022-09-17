import json
from flask_restful import Api, Resource, reqparse
from connect import host, user, password, db_name
import psycopg2



class Users(Resource):
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
                    cursor.execute("""SELECT * from users;""")
                    data = cursor.fetchall()
                    for row in data:
                        result = {}
                        result["id"] = row[0]
                        result["login"] = row[1]
                        result["password"] = row[2]
                        result["email"] = row[3]
                        result["first_name"] = row[4]
                        result["last_name"] = row[5]
                        result["status"] = row[6]
                        jsonData.append(result)
                return jsonData, 200
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")