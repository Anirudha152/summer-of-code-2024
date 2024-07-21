from database import Customer, db
from flask import Blueprint, request
import flask_login
customer = Blueprint('customer', __name__)


@customer.route('/create', methods=['POST'])
@flask_login.login_required
def create_customer():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    try:
        c_ID = data['c_ID']
        c_name = data['c_name']
        c_email = data['c_email']
        c_contact = data['c_contact']
        new_customer = Customer(c_ID=c_ID, c_name=c_name, c_email=c_email, c_contact=c_contact)
        db.session.add(new_customer)
        db.session.commit()
        return {"message": "Customer created successfully"}, 201
    except:
        return {"error": "Invalid request body"}, 400


@customer.route('/get', methods=['GET'])
@flask_login.login_required
def get_customer():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    ID = None
    email = None
    if 'c_ID' in dict(request.get_json()).keys():
        ID = dict(request.get_json())['c_ID']
    elif 'c_email' in dict(request.get_json()).keys():
        email = dict(request.get_json())['c_email']
    if ID is not None:
        if ID == 'all':
            customers = Customer.query.all()
            customer_list = []
            for c in customers:
                customer_list.append({'c_ID': c.c_ID, 'c_name': c.c_name, 'c_email': c.c_email, 'c_contact': c.c_contact})
            return {"customers": customer_list}, 200
        else:
            customer = Customer.query.filter_by(c_ID=ID).first()
            if customer:
                return {'c_ID': customer.c_ID, 'c_name': customer.c_name, 'c_email': customer.c_email, 'c_contact': customer.c_contact}, 200
            else:
                return {"error": "Customer not found"}, 404
    elif email is not None:
        customer = Customer.query.filter_by(c_email=email).first()
        if customer:
            return {'c_ID': customer.c_ID, 'c_name': customer.c_name, 'c_email': customer.c_email, 'c_contact': customer.c_contact}, 200
        else:
            return {"error": "Customer not found"}, 404
    else:
        return {"error": "Invalid request body"}, 400


@customer.route('/update', methods=['PUT'])
@flask_login.login_required
def update_customer():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    c_ID = data['c_ID']
    customer = Customer.query.filter_by(c_ID=c_ID).first()
    if customer:
        if 'c_name' in data.keys():
            customer.c_name = data['c_name']
        if 'c_email' in data.keys():
            customer.c_email = data['c_email']
        if 'c_contact' in data.keys():
            customer.c_contact = data['c_contact']
        db.session.commit()
        return {"message": "Customer updated successfully"}, 200
    else:
        return {"error": "Customer not found"}, 404


@customer.route('/delete', methods=['DELETE'])
@flask_login.login_required
def delete_customer():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    c_ID = dict(request.get_json())['c_ID']
    customer = Customer.query.filter_by(c_ID=c_ID).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {"message": "Customer deleted successfully"}, 200
    else:
        return {"error": "Customer not found"}, 404