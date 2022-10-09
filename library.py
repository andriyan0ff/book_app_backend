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
            parser.add_argument("users")
            parser.add_argument("book")
            params = parser.parse_args()
            if str(params["visible"]) == "all" and str(params["users"]) == "" and str(params["book"]) == "":
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM library;""")
                    data = cursor.fetchall()
                    for row in data:
                        result = {}
                        result["id"] = row[0]
                        result["book"] = row[1]
                        result["users"] = row[2]
                        result["status"] = row[3]
                        jsonData.append(result)
                return jsonData, 200
            elif str(params["visible"]) == "" and str(params["users"]) != "" and str(params["book"]) == "":
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM library WHERE users = '""" + str(params["users"]) + """';""")
                    data = cursor.fetchall()
                    if len(data) > 0:
                        for row in data:
                            result = {}
                            result["id"] = row[0]
                            result["book"] = row[1]
                            result["users"] = row[2]
                            result["status"] = row[3]
                            jsonData.append(result)
                        return jsonData, 200
            elif str(params["visible"]) == "" and str(params["users"]) == "" and str(params["book"]) != "":
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM library WHERE book = '""" + str(params["book"]) + """';""")
                    data = cursor.fetchall()
                    if len(data) > 0:
                        for row in data:
                            result = {}
                            result["id"] = row[0]
                            result["book"] = row[1]
                            result["users"] = row[2]
                            result["status"] = row[3]
                            jsonData.append(result)
                        return jsonData, 200
                    else:
                        return "no books", 404
            else:
                    return "sorry", 400
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    def put(self):
        try:
            statusUpdate = {
                "status": "update"
            }
            statusCreate = {
                "status": "create"
            }
            statusError = {
                "status": "Error"
            }
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            parser = reqparse.RequestParser()
            parser.add_argument("book")
            parser.add_argument("users")
            parser.add_argument("status")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM library WHERE book = '""" + str(params["book"]) + """'
                               AND users = '""" + str(params["users"]) + """';
                               """)
                data = cursor.fetchall()
                if len(data) != 0:
                    cursor.execute("""
                                    UPDATE library SET
                                    book = '""" + str(params["book"]) + """',
                                    status = '""" + str(params["status"]) + """'
                                    WHERE users = '""" + str(params["users"]) + """';
                                    """)
                    return statusUpdate, 200
                else:
                    cursor.execute("""
                                    INSERT INTO library (book, users, status)
                                    VALUES
                                    ('""" + str(params["book"]) + """',
                                    '""" + str(params["users"]) + """',
                                    '""" + str(params["status"]) + """');
                                    """)
                    return statusCreate, 201
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
            return statusError, 400
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")