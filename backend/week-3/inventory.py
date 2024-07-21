from database import InventoryItem, db
from flask import Blueprint, request
import flask_login
inventory_item = Blueprint('inventory_item', __name__)


@inventory_item.route('/add', methods=['POST'])
@flask_login.login_required
def add_inventory_item():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    try:
        Item_SKU = data['Item_SKU']
        Item_Name = data['Item_Name']
        Item_Description = data['Item_Description']
        Item_Price = data['Item_Price']
        Item_Qty = data['Item_Qty']
        new_inventory_item = InventoryItem(Item_SKU=Item_SKU, Item_Name=Item_Name, Item_Description=Item_Description, Item_Price=Item_Price, Item_Qty=Item_Qty)
        db.session.add(new_inventory_item)
        db.session.commit()
        return {"message": "Inventory item added successfully"}, 201
    except:
        return {"error": "Invalid request body"}, 400


@inventory_item.route('/get', methods=['GET'])
@flask_login.login_required
def get_inventory_item():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    SKU = dict(request.get_json())['SKU']
    if SKU == 'all':
        items = InventoryItem.query.all()
        item_list = []
        for i in items:
            item_list.append({'Item_SKU': i.Item_SKU, 'Item_Name': i.Item_Name, 'Item_Description': i.Item_Description, 'Item_Price': i.Item_Price, 'Item_Qty': i.Item_Qty})
        return {"inventory_items": item_list}, 200
    else:
        item = InventoryItem.query.filter_by(Item_SKU=SKU).first()
        if item:
            return {'Item_SKU': item.Item_SKU, 'Item_Name': item.Item_Name, 'Item_Description': item.Item_Description, 'Item_Price': item.Item_Price, 'Item_Qty': item.Item_Qty}, 200
        else:
            return {"error": "Inventory item not found"}, 404


@inventory_item.route('/update', methods=['PUT'])
@flask_login.login_required
def update_inventory_item():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    data = dict(request.get_json())
    Item_SKU = data['Item_SKU']
    item = InventoryItem.query.filter_by(Item_SKU=Item_SKU).first()
    if item:
        if data['Item_Name']:
            item.Item_Name = data['Item_Name']
        if data['Item_Description']:
            item.Item_Description = data['Item_Description']
        if data['Item_Price']:
            item.Item_Price = data['Item_Price']
        if data['Item_Qty']:
            item.Item_Qty = data['Item_Qty']
        db.session.commit()
        return {"message": "Inventory item updated successfully"}, 200
    else:
        return {"error": "Inventory item not found"}, 404


@inventory_item.route('/delete', methods=['DELETE'])
@flask_login.login_required
def delete_inventory_item():
    if not flask_login.current_user.s_isApproved:
        return {"error": "Unauthorized access"}, 401
    Item_SKU = dict(request.get_json())['Item_SKU']
    item = InventoryItem.query.filter_by(Item_SKU=Item_SKU).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return {"message": "Inventory item deleted successfully"}, 200
    else:
        return {"error": "Inventory item not found"}, 404


