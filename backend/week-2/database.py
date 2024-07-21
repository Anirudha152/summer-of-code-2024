from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()


class Staff(db.Model):
    s_ID = db.Column(db.String, primary_key=True)
    s_name = db.Column(db.String)
    s_email = db.Column(db.String)
    s_isAdmin = db.Column(db.Boolean)
    s_contact = db.Column(db.String)


class Transaction(db.Model):
    t_ID = db.Column(db.String, primary_key=True)
    c_ID = db.Column(db.String, db.ForeignKey('customer.c_ID'))
    s_ID = db.Column(db.String, db.ForeignKey('staff.s_ID'))
    item_SKU = db.Column(db.String, db.ForeignKey('inventory_item.Item_SKU'))
    t_date = db.Column(db.DateTime)
    t_amount = db.Column(db.Float)
    t_category = db.Column(db.String)


class Customer(db.Model):
    c_ID = db.Column(db.String, primary_key=True)
    c_name = db.Column(db.String)
    c_email = db.Column(db.String, index=True)

    @validates('c_email')
    def validate_email(self, key, email):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Provided email is not in valid format"
        return email

    c_contact = db.Column(db.String)


class InventoryItem(db.Model):
    Item_SKU = db.Column(db.String, primary_key=True, index=True)
    Item_Name = db.Column(db.String)
    Item_Description = db.Column(db.String)
    Item_Price = db.Column(db.Float)

    @validates('Item_Price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return price

    Item_Qty = db.Column(db.Integer)

    @validates('Item_Qty')
    def validate_qty(self, key, qty):
        if qty < 0:
            raise ValueError("Quantity must be greater than or equal to 0")
        return qty
