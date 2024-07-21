from database import db
import create_app
from staff import staff
from customer import customer
from inventory import inventory_item
from transactions import transaction
app = create_app.create_app()
db.init_app(app)

app.register_blueprint(staff, url_prefix='/staff')
app.register_blueprint(customer, url_prefix='/customer')
app.register_blueprint(inventory_item, url_prefix='/inventory')
app.register_blueprint(transaction, url_prefix='/transaction')


if __name__ == '__main__':
    app.run(debug=True)
