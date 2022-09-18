from flask import Flask
from flask_restful import Api, Resource, reqparse
from users import Users
from country import Country


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Users, "/users", "/users/", "/users/<int:id>")
    api.add_resource(Country, "/users", "/users/", "/country/<int:id>")
    app.run(debug=True)