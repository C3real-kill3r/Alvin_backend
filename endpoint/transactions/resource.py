from flask import request, jsonify
from itsdangerous import json
from app import app, db

import datetime

from endpoint.transactions.model import Category, Transaction, transactions_schema, transaction_schema
from utils.commons import check_admin, token_required

# Create a transaction
@app.route('/transaction', methods=['POST'])
@token_required
def add_transaction(current_user):
    print(current_user)
    try:
        transaction = request.get_json()
        category = transaction['category']
        if category and category in [e.value for e in Category]:
            category = Category(category)
        else:
            return jsonify({'message': 'invalid category'})
        category = Category(category)
        amount = transaction['amount']
        date = datetime.datetime.utcnow()
        description = transaction['description']
        merchant = transaction['merchant']
        new_transaction = Transaction(amount, category, date, description, merchant, current_user.id)
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'transaction created successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})


# Get all transactions
@app.route('/transaction', methods=['GET'])
@token_required
def get_transactions(current_user):
    try:
        if check_admin(current_user):
            transactions = Transaction.query.all()
            result = transactions_schema.dump(transactions)
            for transaction in result:
                transaction['category'] = transaction['category'].name
            return jsonify(result)
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id)
            result = transactions_schema.dump(transactions)
            for transaction in result:
                transaction['category'] = transaction['category'].name
            return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)})


# Get a single transaction
@app.route('/transaction/<id>', methods=['GET'])
@token_required
def get_transaction(current_user, id):
    try:
        transaction = Transaction.query.get(id)
        transaction.category = transaction.category.name
        if check_admin(current_user) or transaction.user_id == current_user.id:
            return transaction_schema.jsonify(transaction)
        elif transaction.user_id != current_user.id:
            return jsonify({'message': 'unauthorized'})
    except Exception as e:
        return jsonify({'message': str(e)})


# Update a transaction
@app.route('/transaction/<id>', methods=['PUT'])
@token_required
def update_transaction(current_user, id):
    try:
        transaction = Transaction.query.get(id)
        if check_admin(current_user) or transaction.user_id == current_user.id:
            transaction_data = request.get_json()
            if transaction_data['category'] and transaction_data['category'] in [e.value for e in Category]:
                category = Category(transaction_data['category'])
                transaction.category = category
            elif transaction_data['category'] and transaction_data['category'] not in [e.value for e in Category]:
                return jsonify({'message': 'invalid category'})
            transaction.amount = transaction_data['amount']
            transaction.date = datetime.datetime.utcnow()
            transaction.description = transaction_data['description']
            transaction.merchant = transaction_data['merchant']
            db.session.commit()
            return jsonify({'message': 'transaction updated successfully'})
        elif transaction.user_id != current_user.id:
            return jsonify({'message': 'unauthorized'})
    except Exception as e:
        return jsonify({'message': str(e)})


# get all transactions for a category
@app.route('/transaction/category/<category>/', methods=['GET'])
@token_required
def get_transactions_by_category(current_user, category):
    try:
        category = Category(category)
        if check_admin(current_user):
            transactions = Transaction.query.filter_by(category=category)
            for transaction in transactions:
                transaction.category = transaction.category.name
            result = transactions_schema.dump(transactions)
            return jsonify(result)
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id, category=category)
            for transaction in transactions:
                transaction.category = transaction.category.name
            result = transactions_schema.dump(transactions)
            return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)})


# get the total amount transactions for a category
@app.route('/transaction/category/<category>/total', methods=['GET'])
@token_required
def get_total_transactions_by_category(current_user, category):
    try:
        category = Category(category)
        if check_admin(current_user):
            transactions = Transaction.query.filter_by(category=category)
            total = 0
            for transaction in transactions:
                total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id, category=category)
            total = 0
            for transaction in transactions:
                total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
    except Exception as e:
        return jsonify({'message': str(e)})


# get the total amount transactions for a category for a specific month
@app.route('/transaction/category/<category>/total/<month>', methods=['GET'])
@token_required
def get_total_transactions_by_category_month(current_user, category, month):
    try:
        category = Category(category)
        if check_admin(current_user):
            transactions = Transaction.query.filter_by(category=category)
            total = 0
            for transaction in transactions:
                if transaction.date.month == int(month):
                    total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id, category=category)
            total = 0
            for transaction in transactions:
                if transaction.date.month == int(month):
                    total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
    except Exception as e:
        return jsonify({'message': str(e)})


# get the total amount transactions for a category for a specific period
@app.route('/transaction/category/<category>/total/period', methods=['GET'])
@token_required
def get_total_transactions_by_category_period(current_user, category):
    try:
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        category = Category(category)
        if check_admin(current_user):
            transactions = Transaction.query.filter_by(category=category)
            total = 0
            for transaction in transactions:
                if transaction.date >= datetime.datetime.strptime(start_date, '%Y-%m-%d') and transaction.date <= datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                    total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id, category=category)
            total = 0
            for transaction in transactions:
                if transaction.date >= datetime.datetime.strptime(start_date, '%Y-%m-%d') and transaction.date <= datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                    total += transaction.amount
            return jsonify({'total': total, 'category': category.name})
    except:
        return jsonify({'message': 'invalid date'})


# get the total amount transactions for every category seperately and return a list of dictionaries
@app.route('/transaction/total/', methods=['GET'])
@token_required
def get_total_transactions(current_user):
    try:
        categories = [e.value for e in Category]
        if check_admin(current_user):
            total_transactions = []
            for category in categories:
                category = Category(category)
                transactions = Transaction.query.filter_by(category=category)
                total = 0
                for transaction in transactions:
                    total += transaction.amount
                total_transactions.append({'category': category.name, 'total': total})
            return jsonify(total_transactions)
        else:
            total_transactions = []
            for category in categories:
                category = Category(category)
                transactions = Transaction.query.filter_by(user_id=current_user.id, category=category)
                total = 0
                for transaction in transactions:
                    total += transaction.amount
                total_transactions.append({'category': category.name, 'total': total})
            return jsonify(total_transactions)
    except Exception as e:
        return jsonify({'message': str(e)})

# Delete a transaction
@app.route('/transaction/<id>', methods=['DELETE'])
@token_required
def delete_transaction(current_user, id):
    try:
        transaction = Transaction.query.get(id)
        transaction.category = transaction.category.name
        if check_admin(current_user) or transaction.user_id == current_user.id:
            db.session.delete(transaction)
            db.session.commit()
            return jsonify({'message': 'transaction deleted successfully'})
        elif transaction.user_id != current_user.id:
            return jsonify({'message': 'unauthorized'})
    except:
        return jsonify({'message': 'transaction not found'})


# delete all transactions
@app.route('/transaction', methods=['DELETE'])
@token_required
def delete_all_transactions(current_user):
    try:
        if check_admin(current_user):
            transactions = Transaction.query.all() 
            for transaction in transactions:
                transaction.category = transaction.category.name
                db.session.delete(transaction)
                db.session.commit()
            return jsonify({'message': 'all transactions deleted successfully'})
        else:
            transactions = Transaction.query.filter_by(user_id=current_user.id)
            for transaction in transactions:
                transaction.category = transaction.category.name
                db.session.delete(transaction)
                db.session.commit()
            return jsonify({'message': 'all transactions deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})