from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.slbdvralwtckymtknwan:7oa5mvhVVY16QLRJ@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'

db = SQLAlchemy(app)


class InventoryItem(db.Model):
    Item_SKU = db.Column(db.String, primary_key=True, index=True)
    Item_Name = db.Column(db.String)
    Item_Description = db.Column(db.String)
    Item_Price = db.Column(db.Float)
    @validates('Item_Price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
    Item_Qty = db.Column(db.Integer)
    @validates('Item_Qty')
    def validate_qty(self, key, qty):
        if qty < 0:
            raise ValueError("Quantity must be greater than or equal to 0")


class Customer(db.Model):
    c_ID = db.Column(db.String, primary_key=True)
    c_name = db.Column(db.String)
    c_email = db.Column(db.String, index=True)
    @validates('c_email')
    def validate_email(self, key, email):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Provided email is not in valid format"
        return email
    c_contact = db.Column(db.String)


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


with app.app_context():
    db.create_all()


def seed_data():
    # Create some InventoryItems
    item3 = InventoryItem(Item_SKU='sku3', Item_Name='Item 3', Item_Description='This is item 3', Item_Price=30.0, Item_Qty=300)
    item4 = InventoryItem(Item_SKU='sku4', Item_Name='Item 4', Item_Description='This is item 4', Item_Price=40.0, Item_Qty=400)


    # Create some Customers
    customer3 = Customer(c_ID='c3', c_name='Customer 3', c_email='customer3@example.com', c_contact='3434567890')
    customer4 = Customer(c_ID='c4', c_name='Customer 4', c_email='customer4@example.com', c_contact='0987654343')


    # Create some Staff
    staff3 = Staff(s_ID='s3', s_name='Staff 3', s_email='staff3@example.com', s_isAdmin=True, s_contact='3333333333')
    staff4 = Staff(s_ID='s4', s_name='Staff 4', s_email='staff4@example.com', s_isAdmin=False, s_contact='4444444444')

    # Create some Transactions
    from datetime import datetime
    transaction3 = Transaction(t_ID='t3', c_ID='c3', s_ID='s3', item_SKU='sku3', t_date=datetime.now(), t_amount=300.0, t_category='Category 3')
    transaction4 = Transaction(t_ID='t4', c_ID='c4', s_ID='s4', item_SKU='sku4', t_date=datetime.now(), t_amount=400.0, t_category='Category 4')

    # Add and commit the instances to the database
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(staff3)
    db.session.add(staff4)
    db.session.add(transaction3)
    db.session.add(transaction4)
    db.session.commit()


# Call the function to seed the data
with app.app_context():
    seed_data()