from flask_restful import Resource, reqparse
from connect import host, user, password, db_name
import psycopg2
import logging

class Status(Resource):
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
                    cursor.execute("""SELECT * FROM status;""")
                    data = cursor.fetchall()
                    for row in data:
                        result = {}
                        result["id"] = row[0]
                        result["name"] = row[1]
                        jsonData.append(result)
                return jsonData, 200
            if id > 0:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM status WHERE id = '"""+str(id)+"""';""")
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
            logging.warning(ex)
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
                cursor.execute("""SELECT * FROM status WHERE name = '""" + str(params["name"]) + """';""")
                data = cursor.fetchall()
                if len(data) == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO status (name)
                            VALUES
                            ('"""+ str(params["name"]) +"""');""")
                    return "New status created!", 201
                else:
                    return "A status with this name already exists", 409
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
            logging.warning(ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def put(self):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("id")
            parser.add_argument("name")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM status WHERE id = '""" + str(params["id"]) + """';""")
                data = cursor.fetchall()
                if len(data) != 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """UPDATE status SET name = '""" + str(params["name"]) + """' 
                            WHERE id = '""" + str(params["id"]) + """';""")
                    return "Status id = " + params["id"] + " Updated", 200
                else:
                    return "Status with this id does not exist", 404
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
            logging.warning(ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def delete(self):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("id")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM status WHERE id = '""" + str(params["id"]) + """';""")
                data = cursor.fetchall()
                if len(data) != 0:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                        UPDATE library SET status = NULL WHERE status = '""" + str(params["id"]) + """';
                        DELETE FROM status WHERE id = '""" + str(params["id"]) + """';
                        """)
                    return "Status id = " + (params["id"]) + " delete!", 200
                else:
                    return "Status with this id not found", 404
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
            logging.warning(ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")