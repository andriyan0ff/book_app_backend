from flask import Flask
from flask_restful import Api
from users import Users
from country import Country
from city import City
from authors import Authors
from login import Login
from category import Category
from status import Status
from books import Books
from library import Library
from version import Version
from st_transactions import StTransactions


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Users, "/users", "/users/", "/users/<int:id>")
    api.add_resource(Country, "/country", "/country/", "/country/<int:id>")
    api.add_resource(City, "/city", "/city/", "/city/<int:id>")
    api.add_resource(Authors, "/authors", "/authors/", "/authors/<int:id>")
    api.add_resource(Login, "/login", "/login/")
    api.add_resource(Category, "/category", "/category/", "/category/<int:id>")
    api.add_resource(Status, "/status", "/status/", "/status/<int:id>")
    api.add_resource(Books, "/books", "/books/", "/books/<int:id>")
    api.add_resource(Library, "/library", "/library/")
    api.add_resource(Version, "/v", "/v/")
    api.add_resource(StTransactions, "/statrans", "/statrans/")
    app.run(debug=True)