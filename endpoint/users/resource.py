from flask import request, jsonify
from itsdangerous import json
from werkzeug.security import generate_password_hash,check_password_hash
from app import app, db

import jwt
import datetime
import uuid

from endpoint.users.model import User, UserSchema, users_schema
from utils.commons import check_admin, token_required

# register user
@app.route('/user', methods=['POST'])
def add_user():
    try:
        user = request.get_json()
        hashed_password = generate_password_hash(user['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), name=user['name'], email=user['email'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user created successfully'})
    except Exception as e:
        if e.__class__.__name__ == 'IntegrityError':
            return jsonify({'message': 'email already exists'})
        return jsonify({'message': str(e)})


# login user
@app.route('/user/login', methods=['POST'])
def login_user():
    try:
        user = request.get_json()
        email = user['email']
        password = user['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            token = jwt.encode({'public_id': user.public_id, 'user_type': user.admin , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})
        return jsonify({'message': 'password or email is incorrect'})
    except Exception as e:
        return jsonify({'message': str(e)})

# logout a user
@app.route('/user/logout', methods=['GET'])
@token_required
def logout_user():
    request.headers["x-access-tokens"] = ""
    return jsonify({'message': 'logged out successfully'})


# get user
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    try:
        if not check_admin(current_user):
            user = User.query.filter_by(public_id=current_user.public_id).first()
            user_schema = UserSchema()
            user_data = user_schema.dump(user)
            return jsonify({'user': user_data})
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)})

# update user
@app.route('/user/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user or (not check_admin(current_user) and current_user.public_id != user.public_id):
            return jsonify({'message': 'user not found'})
        user.name = request.get_json()['name']
        user.email = request.get_json()['email']
        user.password = generate_password_hash(request.get_json()['password'], method='sha256')
        db.session.commit()
        return jsonify({'message': 'user updated successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})

# delete user
@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user or (not check_admin(current_user) and current_user.public_id != user.public_id):
            return jsonify({'message': 'user not found'})
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})
