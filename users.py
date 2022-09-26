from flask_restful import Resource, reqparse
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
                        result["first_name"] = row[1]
                        result["last_name"] = row[2]
                        result["date_birth"] = row[3]
                        result["email"] = row[4]
                        result["telegram"] = row[5]
                        result["phone"] = row[6]
                        result["country"] = row[7]
                        result["city"] = row[8]
                        result["city_index"] = row[9]
                        result["login"] = row[10]
                        result["password"] = row[11]
                        jsonData.append(result)
                return jsonData, 200
            if id > 0:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * from users where id = """+str(id)+""";""")
                    data = cursor.fetchall()
                    if len(data) > 0:
                        for row in data:
                            result = {}
                            result["id"] = row[0]
                            result["first_name"] = row[1]
                            result["last_name"] = row[2]
                            result["date_birth"] = row[3]
                            result["email"] = row[4]
                            result["telegram"] = row[5]
                            result["phone"] = row[6]
                            result["country"] = row[7]
                            result["city"] = row[8]
                            result["city_index"] = row[9]
                            result["login"] = row[10]
                            result["password"] = row[11]
                            jsonData.append(result)
                        return jsonData, 200
                    else:
                        return "User with this id does not exist", 404
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
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
            parser.add_argument("first_name")
            parser.add_argument("last_name")
            parser.add_argument("date_birth")
            parser.add_argument("email")
            parser.add_argument("telegram")
            parser.add_argument("phone")
            parser.add_argument("country")
            parser.add_argument("city")
            parser.add_argument("city_index")
            parser.add_argument("login")
            parser.add_argument("password")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * from users where id = """ + str(params["id"]) + """;""")
                data = cursor.fetchall()
                if len(data) != 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """UPDATE users SET
                            first_name = '"""+ str(params["first_name"]) +"""',
                            last_name = '"""+ str(params["last_name"]) +"""',
                            date_birth = '"""+ str(params["date_birth"]) +"""',
                            email = '"""+ str(params["email"]) +"""',
                            telegram = '"""+ str(params["telegram"]) +"""',
                            phone = '"""+ str(params["phone"]) +"""',
                            country = """+ params["country"] +""",
                            city = """+ params["city"] +""",
                            city_index = '"""+ str(params["city_index"]) +"""',
                            login = '"""+ str(params["login"]) +"""',
                            password = '"""+ str(params["password"]) +"""'
                             WHERE id = """+ str(params["id"]) +""";""")
                    return "User id = " + params["id"] + " Updated", 200
                else:
                    return "User with this id does not exist", 404
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
            parser.add_argument("first_name")
            parser.add_argument("last_name")
            parser.add_argument("date_birth")
            parser.add_argument("email")
            parser.add_argument("telegram")
            parser.add_argument("phone")
            parser.add_argument("country")
            parser.add_argument("city")
            parser.add_argument("city_index")
            parser.add_argument("login")
            parser.add_argument("password")
            params = parser.parse_args()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM users WHERE login = '""" + str(params["login"]) + """';""")
                data = cursor.fetchall()
                if len(data) == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO users (first_name, last_name, date_birth, email, telegram, phone, country, city, city_index, login, password)
                            VALUES
                            ('"""+ str(params["first_name"]) +"""',
                            '"""+ str(params["last_name"]) +"""',
                            '"""+ str(params["date_birth"]) +"""',
                            '"""+ str(params["email"]) +"""',
                            '"""+ str(params["telegram"]) +"""',
                            '"""+ str(params["phone"]) +"""',
                            """+ params["country"] +""",
                            """+ params["city"] +""",
                            '"""+ str(params["city_index"]) +"""',
                            '"""+ str(params["login"]) +"""',
                            '"""+ str(params["password"]) +"""')
                            ;""")
                    return "New user created!", 201
                else:
                    return "User with this login already exists", 409
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
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
                cursor.execute("""SELECT * FROM users WHERE id = '""" + str(params["id"]) + """';""")
                data = cursor.fetchall()
                if len(data) != 0:
                    with connection.cursor() as cursor:
                        cursor.execute("""DELETE FROM users WHERE id = '""" + str(params["id"]) + """';""")
                    return "User id = " + (params["id"]) + " delete!", 200
                else:
                    return "User with this login does not exist", 404
        except Exception as ex:
            print("[ERROR] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")