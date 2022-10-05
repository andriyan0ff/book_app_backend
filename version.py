from flask_restful import Resource

class Version(Resource):
    def get(self):
        otvet = {
            "version": 1.01
        }
        return otvet, 200