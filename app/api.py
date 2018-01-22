import re

from flask import request, Response
from bson.json_util import dumps
from flask_restful import Api, Resource

from app.models import User, Sale
from app import app


class UsersResource(Resource):
    def get(self, email=None):
        if email:
            user = User.query.filter(User.email == email).first()
            if user:
                return Response(dumps(user.to_dict()), status=200, mimetype='application/json')
            return Response(dumps('Not Found'), status=404, mimetype='application/json')

        users = User.query.all()
        return Response(dumps([u.to_dict() for u in users]),
                        status=200, mimetype='application/json')

    def post(self):
        data = request.get_json()
        if not data:
            return Response(dumps({'ERROR': 'no data'}), status=204, mimetype='application/json')

        errors = []
        email = data.get('email')
        if not email:
            errors.append('email is required')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append('invalid email')

        if not data.get('name'):
            errors.append('name is required')

        if not data.get('last_name'):
            errors.append('last_name is required')

        if errors:
            return Response(dumps(errors), status=400, mimetype='application/json')

        if User.query.filter(User.email == email).first():
            return Response('User already exists', status=409, mimetype='application/json')

        user = User(name=data.get('name'), last_name=data.get('last_name'),
                    email=email, address=data.get('address'), approved=False, sales=[])
        user.save()
        return Response(dumps(user.to_dict()), status=201, mimetype='application/json')

    def put(self):
        data = request.get_json()
        if not data:
            return Response('No data', status=204, mimetype='application/json')

        email = data.get('email')
        if not email:
            return Response(dumps('Email is required for searching'), status=204,
                            mimetype='application/json')

        user = User.query.filter(User.email == email).first()
        if not user:
            return Response('Not Found', status=404, mimetype='application/json')

        user.name = data.get('name') if data.get('name') else user.name
        user.last_name = data.get('last_name') if data.get('last_name') else user.last_name
        user.address = data.get('address') if data.get('address') else user.address
        user.save()
        return Response(dumps(user.to_dict()), status=200, mimetype='application/json')


api = Api(app)
api.add_resource(UsersResource, '/api/users', endpoint="users")
api.add_resource(UsersResource, "/api/users/<string:email>", endpoint="user")


@app.route('/api/approve_user/<string:email>', methods=['GET'])
def approve_user(email):
    user = User.query.filter(User.email == email).first()
    if user:
        user.approved = True
        user.save()
        return Response(dumps(user.to_dict()), status=200, mimetype='application/json')
    return Response('Not Found', status=404, mimetype='application/json')


@app.route('/api/deactivate_user/<string:email>', methods=['GET'])
def deactivate_user(email):
    user = User.query.filter(User.email == email).first()
    if user:
        user.approved = False
        user.save()
        return Response(dumps(user.to_dict()), status=200, mimetype='application/json')
    return Response('Not Found', status=404, mimetype='application/json')


@app.route('/api/users/save_sale', methods=['POST'])
def save_sale():
    data = request.get_json()
    if not data:
        return Response('No data', status=204, mimetype='application/json')

    errors = []
    email = data.get('user_email')
    if not email:
        errors.append('user_email is required')

    uuid = data.get('uuid')
    if not uuid:
        errors.append('uuid is required')

    if not data.get('amount'):
        errors.append('amount is required')

    if not data.get('date'):
        errors.append('date is required')

    if errors:
        return Response(dumps(errors), status=400, mimetype='application/json')

    user = User.query.filter(User.email == email).first()
    if not user:
        return Response('Not Found', status=404, mimetype='application/json')

    if not user.approved:
        return Response('Error, user is not approved', status=400, mimetype='application/json')

    if uuid in (sale.uuid for sale in user.sales):
        return Response('Sale already saved', status=400, mimetype='application/json')

    user.sales.append(Sale(uuid=uuid, amount=data.get('amount'),
                           date=data.get('date'), approved=True))
    user.save()
    return Response(dumps(user.to_dict()), status=201, mimetype='application/json')


@app.route('/api/deactivate_sale/<string:uuid>', methods=['GET'])
def deactivate_sale(uuid):
    users = User.query.all()
    sale = None
    for u in users:
        sale = u.get_sale(uuid)
        if sale:
            user = u
            break

    if sale:
        sale.approved = False
        sale.save()
        user.save()
        return Response(dumps(sale.to_dict()), status=200, mimetype='application/json')
    return Response('Not Found', status=404, mimetype='application/json')


@app.route('/api/sales/<string:email>', methods=['GET'])
def sales(email):
    user = User.query.filter(User.email == email).first()
    if not user:
        return Response(dumps('Not Found'), status=404, mimetype='application/json')

    sales_list = [sale.to_dict() for sale in user.sales]
    return Response(dumps(sales_list), status=200, mimetype='application/json')

