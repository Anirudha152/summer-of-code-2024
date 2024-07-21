from database import Staff, db
from flask import Blueprint, request
staff = Blueprint('staff', __name__)


@staff.route('/register', methods=['POST'])
def register_staff():
    data = dict(request.get_json())
    try:
        s_ID = data['s_ID']
        s_name = data['s_name']
        s_email = data['s_email']
        s_isAdmin = data['s_isAdmin']
        s_contact = data['s_contact']
        new_staff = Staff(s_ID=s_ID, s_name=s_name, s_email=s_email, s_isAdmin=s_isAdmin, s_contact=s_contact)
        db.session.add(new_staff)
        db.session.commit()
        return {"message": "Staff registered successfully"}, 201
    except:
        return {"error": "Invalid request body"}, 400


@staff.route('/get', methods=['GET'])
def get_staff():
    ID = dict(request.get_json())['ID']
    if ID == 'all':
        staff = Staff.query.all()
        staff_list = []
        for s in staff:
            staff_list.append({'s_ID': s.s_ID, 's_name': s.s_name, 's_email': s.s_email, 's_isAdmin': s.s_isAdmin, 's_contact': s.s_contact})
        return {"staff": staff_list}, 200
    else:
        staff = Staff.query.filter_by(s_ID=ID).first()
        if staff:
            return {'s_ID': staff.s_ID, 's_name': staff.s_name, 's_email': staff.s_email, 's_isAdmin': staff.s_isAdmin, 's_contact': staff.s_contact}, 200
        else:
            return {"error": "Staff not found"}, 404


@staff.route('/update', methods=['PUT'])
def update_staff():
    data = dict(request.get_json())
    s_ID = data['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if staff:
        if 's_name' in data.keys():
            staff.s_name = data['s_name']
        if 's_email' in data.keys():
            staff.s_email = data['s_email']
        if 's_isAdmin' in data.keys():
            staff.s_isAdmin = data['s_isAdmin']
        if 's_contact' in data.keys():
            staff.s_contact = data['s_contact']
        db.session.commit()
        return {"message": "Staff updated successfully"}, 200
    else:
        return {"error": "Staff not found"}, 404


@staff.route('/delete', methods=['DELETE'])
def delete_staff():
    s_ID = dict(request.get_json())['s_ID']
    staff = Staff.query.filter_by(s_ID=s_ID).first()
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return {"message": "Staff deleted successfully"}, 200
    else:
        return {"error": "Staff not found"}, 404