from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, init_db, Customer ,Admin ,Product,Shop # Import Customer for testing
from config import Config
from sqlalchemy import text
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Initialize the database
init_db(app)

# ------------------ API Endpoints ------------------

# Endpoint to insert a new customer
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()

    # Log incoming data for debugging
    print("Incoming data:", data)

    # Check for required fields
    if not data or not all(key in data for key in ['name', 'email', 'address', 'phone', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new customer instance
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        address=data['address'],
        phone_number=data['phone'],
        password=data['password'],
    )
    # a = db.session.execute(text("SELECT * FROM customers_5"))
    # results = a.fetchall()
    # print("Query results:", results)

    try:
        db.session.execute(text('INSERT INTO customers_4 (name, email, address, phone_number, password) VALUES (:name, :email, :address, :phone, :password)'),
        {
        'name': data['name'],
        'email': data['email'],
        'address': data['address'],
        'phone': data['phone'],
        'password': data['password'],
        })

        db.session.commit()
        return jsonify({"message": "Customer added successfully", "id": new_customer.customer_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/admins', methods=['POST'])
def add_admin():
    data = request.get_json()

    # Log incoming data for debugging
    print("Incoming data:", data)

    # Check for required fields
    if not data or not all(key in data for key in ['name', 'email', 'phone', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new customer instance
    new_admin = Admin(
        name=data['name'],
        email=data['email'],
        phone_number=data['phone'],
        password=data['password'],
    )
    # a = db.session.execute(text("SELECT * FROM customers_5"))
    # results = a.fetchall()
    # print("Query results:", results)

    try:
        db.session.execute(text('INSERT INTO admins_1 (name, email, password, phone_number) VALUES (:name, :email, :password, :phone)'),
        {
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],
        'phone': data['phone'],
        })

        db.session.commit()
        return jsonify({"message": " added successfully", "id": new_admin.admin_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Log incoming data for debugging
    print("Incoming data:", data)

    # Check for required fields
    if not data or not all(key in data for key in ['name', 'price', 'adminName', 'stock']):
        return jsonify({"error": "Missing required fields"}), 400

    # Verify if admin_name exists in the Admin table
    admin = Admin.query.filter_by(name=data['adminName']).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    print("Admin ID is",admin.admin_id)
    print(datetime.now())
    try:
        # Insert the product using SQLAlchemy
        db.session.execute(
            text('INSERT INTO products_1 (name, description, shop_id, price, stock_quantity, admin_id, added_date) VALUES (:name, :description, :shop_id, :price, :stock_quantity, :admin_id, :added_date)'),
            {
                'name': data['name'],
                'description': data['description'],
                'shop_id': 1,  # Use the shop_id passed in the request
                'price': data['price'],
                'stock_quantity': data['stock'],  # Correct stock quantity
                'admin_id': admin.admin_id,  # Use the admin_id of the found admin
                'added_date': datetime.now()
            }
        )   

        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/api/shop', methods=['POST'])
def add_shop():
    data = request.get_json()
    print("Incoming data:", data)

    # Check for required fields in the request
    required_fields = ['shop_name', 'shop_address', 'phone_number', 'email', 'adminName']
    if not data or not all(key in data for key in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Verify if the admin exists in the Admin table based on adminName
    admin = Admin.query.filter_by(name=data['adminName']).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    print(f"Admin ID for {data['adminName']} is {admin.admin_id}")
    print(datetime.now())

    try:
        # Insert the shop using SQLAlchemy
        db.session.execute(
            text('INSERT INTO shops_1 (shop_name, shop_address, phone_number, email, owner_name, admin_id) VALUES (:shop_name, :shop_address, :phone_number, :email, :owner_name, :admin_id)'),
            {
                'shop_name': data['shop_name'],
                'shop_address': data.get('shop_address', ''),
                'phone_number': data.get('phone_number', ''),
                'email': data.get('email', ''),
                'owner_name': admin.name,
                'admin_id': admin.admin_id  # Use the admin_id of the found admin
            }
        )

        db.session.commit()
        return jsonify({"message": "Shop added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error adding shop: {str(e)}")
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/product_display',methods = ['GET'])
def get_products():
    try:
        products = db.session.execute(text("SELECT product_id,name,description,price,stock_quantity FROM products_1"))
        products_list = [{
            'product_id':product.product_id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock_quantity': product.stock_quantity,
        } for product in products]
        return jsonify({
            'products': products_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/shop_display', methods=['GET'])
def get_shops():
    try:
        shops = db.session.execute(
            text("SELECT shop_id, shop_name, shop_address, phone_number, email, owner_name FROM shops_1")
        )
        shops_list = [{
            'shop_id': shop.shop_id,
            'shop_name': shop.shop_name,
            'shop_address': shop.shop_address,
            'phone_number': shop.phone_number,
            'email': shop.email,
            'owner_name': shop.owner_name
        } for shop in shops]
        
        return jsonify({
            'shops': shops_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
