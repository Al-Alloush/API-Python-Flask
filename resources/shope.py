from flask_restful import Resource, reqparse
from models.shope import ShopeModel
from flask_jwt_extended import(
    jwt_required, 
    fresh_jwt_required
) 
from modifyFunctions import *

class Shope(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        shope = ShopeModel.find_by_name(name)
        if shope:
            return shope.json()
        return {'message': 'shope not found'}, 404

    
    @jwt_required
    @make_secure("admin")
    def post(self, name):
        if ShopeModel.find_by_name(name):
            return {'message': "A shope with name '{}' already exists.".format(name)}, 400

        shope = ShopeModel(name)
        try:
            shope.save_to_db()
        except:
            return {"message": "An error occurred creating the shope."}, 500

        return shope.json(), 201

    @jwt_required
    @make_secure("admin")
    def put(self, name):
        data = Shope.parser.parse_args()
        shope = ShopeModel.find_by_name(name)

        if shope:
            # if this shop exist update, else:
            shope.name = data['new_name']
        else:
            # Create new one
            shope = ShopeModel(data['new_name'])

        shope.save_to_db()

        return shope.json()

    @jwt_required
    @make_secure("admin")
    def delete(self, name):
        shope = ShopeModel.find_by_name(name)
        if shope:
            shope.delete_from_db()

        return {'message': 'Shope deleted'}


class ShopeList(Resource):
    def get(self):
        #return {'shopes': list(map(lambda x: x.json(), ShopeModel.query.all()))}
        # a generally list comprehension, it is a little bit faster, a little bit more readable
        return {'products': [ x.json() for x in ShopeModel.find_all() ]}