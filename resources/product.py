from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.product import ProductModel


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        product = ProductModel.find_by_name(name)
        if product:
            return product.json()
        return {'message': 'product not found'}, 404

    def post(self, name):
        if ProductModel.find_by_name(name):
            return {'message': "A product with name '{}' already exists.".format(name)}, 400

        data = Product.parser.parse_args()

        product = ProductModel(name, data['price'])

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred inserting the product."}, 500

        return product.json(), 201

    def delete(self, name):
        product = ProductModel.find_by_name(name)
        if product:
            product.delete_from_db()
            return {'message': 'product deleted.'}
        return {'message': 'product not found.'}, 404

    def put(self, name):
        data = Product.parser.parse_args()

        product = ProductModel.find_by_name(name)

        if product:
            product.price = data['price']
        else:
            product = ProductModel(name, data['price'])

        product.save_to_db()

        return product.json()


class ProductList(Resource):
    def get(self):
        return {'products': list(map(lambda x: x.json(), ProductModel.query.all()))}