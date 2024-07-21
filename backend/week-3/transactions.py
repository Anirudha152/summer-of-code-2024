from database import Transaction, db
from flask import Blueprint, request
import flask_login
transaction = Blueprint('transaction', __name__)


@transaction.route('/add', methods=['POST'])
@flask_login.login_required
def add_transaction():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    try:
        t_ID = data['t_ID']
        c_ID = data['c_ID']
        s_ID = data['s_ID']
        Item_SKU = data['Item_SKU']
        Item_Qty = data['Item_Qty']
        new_transaction = Transaction(t_ID=t_ID, c_ID=c_ID, s_ID=s_ID, Item_SKU=Item_SKU, Item_Qty=Item_Qty)
        db.session.add(new_transaction)
        db.session.commit()
        return {"message": "Transaction added successfully"}, 201
    except:
        return {"error": "Invalid request body"}, 400


@transaction.route('/get', methods=['GET'])
@flask_login.login_required
def get_transaction():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    ID = dict(request.get_json())['ID']
    if ID == 'all':
        transactions = Transaction.query.all()
        transaction_list = []
        for t in transactions:
            transaction_list.append({'t_ID': t.t_ID, 'c_ID': t.c_ID, 's_ID': t.s_ID, 'Item_SKU': t.Item_SKU, 'Item_Qty': t.Item_Qty})
        return {"transactions": transaction_list}, 200
    else:
        transaction = Transaction.query.filter_by(t_ID=ID).first()
        if transaction:
            return {'t_ID': transaction.t_ID, 'c_ID': transaction.c_ID, 's_ID': transaction.s_ID, 'Item_SKU': transaction.Item_SKU, 'Item_Qty': transaction.Item_Qty}, 200
        else:
            return {"error": "Transaction not found"}, 404


@transaction.route('/update', methods=['PUT'])
@flask_login.login_required
def update_transaction():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    t_ID = data['t_ID']
    transaction = Transaction.query.filter_by(t_ID=t_ID).first()
    if transaction:
        if 'c_ID' in data.keys():
            transaction.c_ID = data['c_ID']
        if 's_ID' in data.keys():
            transaction.s_ID = data['s_ID']
        if 'Item_SKU' in data.keys():
            transaction.Item_SKU = data['Item_SKU']
        if 'Item_Qty' in data.keys():
            transaction.Item_Qty = data['Item_Qty']
        db.session.commit()
        return {"message": "Transaction updated successfully"}, 200
    else:
        return {"error": "Transaction not found"}, 404


@transaction.route('/delete', methods=['DELETE'])
@flask_login.login_required
def delete_transaction():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    t_ID = data['t_ID']
    transaction = Transaction.query.filter_by(t_ID=t_ID).first()
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        return {"message": "Transaction deleted successfully"}, 200
    else:
        return {"error": "Transaction not found"}, 404
