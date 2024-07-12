from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
import uuid

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'shlok123'
jwt = JWTManager(app)

USERS_FILE_PATH = 'users.json'
PRODUCTS_FILE_PATH = 'products.json'
CART_FILE_PATH = 'cart.json'
WISHLIST_FILE_PATH = 'wishlist.json'

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

users = read_json(USERS_FILE_PATH)
products = read_json(PRODUCTS_FILE_PATH)
carts = read_json(CART_FILE_PATH)
wishlists = read_json(WISHLIST_FILE_PATH)

@app.route('/register', methods=['POST'])
def register():
    new_user = request.get_json()
    users.append(new_user)
    write_json(USERS_FILE_PATH, users)
    return jsonify(new_user), 201

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    user = next((user for user in users if user["email"] == credentials["email"] and user["password"] == credentials["password"]), None)
    if user:
        access_token = create_access_token(identity=user["email"])
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad email or password"}), 401

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = next((product for product in products if product["Id"] == id), None)
    return jsonify(product) if product else ("Product not found", 404)

@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    new_product = request.get_json()
    products.append(new_product)
    write_json(PRODUCTS_FILE_PATH, products)
    return jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = next((product for product in products if product["Id"] == id), None)
    if product:
        updated_data = request.get_json()
        product.update(updated_data)
        write_json(PRODUCTS_FILE_PATH, products)
        return jsonify(product)
    return ("Product not found", 404)

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    global products
    products = [product for product in products if product["Id"] != id]
    write_json(PRODUCTS_FILE_PATH, products)
    return "", 204

@app.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_email = get_jwt_identity()
    item = request.get_json()
    user_cart = next((cart for cart in carts if cart["email"] == user_email), None)
    if not user_cart:
        user_cart = {"email": user_email, "items": []}
        carts.append(user_cart)
    user_cart["items"].append(item)
    write_json(CART_FILE_PATH, carts)
    return jsonify(user_cart)

@app.route('/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_email = get_jwt_identity()
    user_cart = next((cart for cart in carts if cart["email"] == user_email), None)
    if user_cart:
        user_cart["items"] = [item for item in user_cart["items"] if item["Id"] != item_id]
        write_json(CART_FILE_PATH, carts)
        return "", 204
    return ("Cart not found", 404)

@app.route('/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user_email = get_jwt_identity()
    item = request.get_json()
    user_wishlist = next((wishlist for wishlist in wishlists if wishlist["email"] == user_email), None)
    if not user_wishlist:
        user_wishlist = {"email": user_email, "items": []}
        wishlists.append(user_wishlist)
    user_wishlist["items"].append(item)
    write_json(WISHLIST_FILE_PATH, wishlists)
    return jsonify(user_wishlist)

@app.route('/wishlist/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(item_id):
    user_email = get_jwt_identity()
    user_wishlist = next((wishlist for wishlist in wishlists if wishlist["email"] == user_email), None)
    if user_wishlist:
        user_wishlist["items"] = [item for item in user_wishlist["items"] if item["Id"] != item_id]
        write_json(WISHLIST_FILE_PATH, wishlists)
        return "", 204
    return ("Wishlist not found", 404)

@app.route('/products/filter', methods=['GET'])
@jwt_required()
def filter_products():
    size = request.args.get('size')
    color = request.args.get('color')
    filtered_products = [product for product in products if (size is None or product.get('Size') == size) and (color is None or product.get('Color') == color)]
    return jsonify(filtered_products)

if __name__ == '__main__':
    app.run(debug=True)
