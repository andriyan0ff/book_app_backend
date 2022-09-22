from flask import Flask
from flask_restful import Api
from users import Users
from country import Country
from city import City
from authors import Authors


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Users, "/users", "/users/", "/users/<int:id>")
    api.add_resource(Country, "/country", "/country/", "/country/<int:id>")
    api.add_resource(City, "/city", "/city/", "/city/<int:id>")
    api.add_resource(Authors, "/authors", "/authors/", "/authors/<int:id>")
    app.run(debug=True)