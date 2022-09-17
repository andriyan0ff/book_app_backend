from flask import Flask
from flask_restful import Api, Resource, reqparse
from users import Users


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Users, "/users", "/users/", "/users/<int:id>")
    app.run(debug=True)