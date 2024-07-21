from database import Staff, db
from flask import Blueprint, request
import flask_login
import dotenv
import os
import bcrypt
staff = Blueprint('staff', __name__)

dotenv.load_dotenv()
salt = os.getenv('SALT').encode('utf-8')


class User(flask_login.UserMixin):
    pass


@staff.route('/login', methods=['POST'])
def login_staff():
    data = dict(request.get_json())
    s_username = data['s_username']
    s_password_e = bcrypt.hashpw(data['s_password'].encode('utf-8'), salt).decode('utf-8')
    staff = Staff.query.filter_by(s_username=s_username).first()
    if staff:
        if staff.s_password == s_password_e:
            flask_login.login_user(staff)
            return {"message": "Login successful"}, 200
        else:
            return {"error": "Invalid password"}, 401
    else:
        return {"error": "Staff not found"}, 404


@staff.route('/logout', methods=['GET'])
@flask_login.login_required
def logout_staff():
    flask_login.logout_user()
    return {"message": "Logout successful"}, 200


@staff.route('/register', methods=['POST'])
def register_staff():
    data = dict(request.get_json())
    try:
        s_ID = data['s_ID']
        s_username = data['s_username']
        s_email = data['s_email']
        s_password_e = bcrypt.hashpw(data['s_password'].encode('utf-8'), salt).decode('utf-8')
        s_contact = data['s_contact']
        new_staff = Staff(s_ID=s_ID, s_username=s_username, s_email=s_email, s_password=s_password_e, s_contact=s_contact, s_isAdmin=False, s_isApproved=False)
        db.session.add(new_staff)
        db.session.commit()
        return {"message": "Staff registered successfully"}, 201
    except:
        return {"error": "Invalid request body"}, 400


@staff.route('/approve', methods=['PUT'])
@flask_login.login_required
def approve_staff():
    user = flask_login.current_user
    if not user.s_isAdmin:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    s_ID = data['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if staff:
        staff.s_isApproved = True
        db.session.commit()
        return {"message": "Staff approved successfully"}, 200
    else:
        return {"error": "Staff not found"}, 404


@staff.route('/promote', methods=['PUT'])
@flask_login.login_required
def promote_to_admin():
    user = flask_login.current_user
    if not user.s_isAdmin:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    s_ID = data['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if staff:
        staff.s_isAdmin = True
        staff.s_isApproved = True
        db.session.commit()
        return {"message": "Staff promoted to admin successfully"}, 200
    else:
        return {"error": "Staff not found"}, 404


@staff.route('/demote', methods=['PUT'])
@flask_login.login_required
def demote_from_admin():
    user = flask_login.current_user
    if not user.s_isAdmin:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    s_ID = data['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if staff:
        staff.s_isAdmin = False
        db.session.commit()
        return {"message": "Staff demoted from admin successfully"}, 200
    else:
        return {"error": "Staff not found"}, 404


@staff.route('/get', methods=['GET'])
@flask_login.login_required
def get_staff():
    ID = dict(request.get_json())['ID']
    if ID == 'all':
        if not flask_login.current_user.s_isAdmin:
            return {"error": "Unauthorized access"}, 401
        staff = Staff.query.all()
        staff_list = []
        for s in staff:
            staff_list.append({'s_ID': s.s_ID, 's_username': s.s_username, 's_email': s.s_email, 's_isAdmin': s.s_isAdmin, 's_isApproved': s.s_isApproved, 's_contact': s.s_contact})
        return {"staff": staff_list}, 200
    else:
        staff = Staff.query.filter_by(s_ID=ID).first()
        if not staff:
            return {"error": "Staff not found"}, 404
        if flask_login.current_user.s_ID != ID and not flask_login.current_user.s_isAdmin:
            return {"error": "Unauthorized access"}, 401
        return {'s_ID': staff.s_ID, 's_username': staff.s_username, 's_email': staff.s_email, 's_isAdmin': staff.s_isAdmin, 's_isApproved': staff.s_isApproved, 's_contact': staff.s_contact}, 200


@staff.route('/update', methods=['PUT'])
# @flask_login.login_required
def update_staff():
    data = dict(request.get_json())
    s_ID = data['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if not staff:
        return {"error": "Staff not found"}, 404
    # if flask_login.current_user.s_ID != s_ID and not flask_login.current_user.s_isAdmin:
    #     return {"error": "Unauthorized access"}, 401
    if 's_username' in data.keys():
        if Staff.query.filter_by(s_username=data['s_username']).first():
            if Staff.query.filter_by(s_username=data['s_username']).first().s_ID != s_ID:
                return {"error": "Username already exists"}, 400
        staff.s_username = data['s_username']
    if 's_password' in data.keys():
        staff.s_password = bcrypt.hashpw(data['s_password'].encode('utf-8'), salt).decode('utf-8')
    if 's_email' in data.keys():
        staff.s_email = data['s_email']
    if 's_contact' in data.keys():
        staff.s_contact = data['s_contact']
    db.session.commit()
    return {"message": "Staff updated successfully"}, 200


@staff.route('/delete', methods=['DELETE'])
@flask_login.login_required
def delete_staff():
    s_ID = dict(request.get_json())['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if not staff:
        return {"error": "Staff not found"}, 404
    if flask_login.current_user.s_ID != s_ID and not flask_login.current_user.s_isAdmin:
        return {"error": "Unauthorized access"}, 401
    db.session.delete(staff)
    db.session.commit()
    return {"message": "Staff deleted successfully"}, 200