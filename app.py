from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt



app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


# App configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Product model (example)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Create a test user with username 'testuser' and password 'testpassword'
hashed_password = bcrypt.generate_password_hash('psd').decode('utf-8')
test_user = User(username='test', password=hashed_password)

# Create a test user with username 'test' and password 'psd'
with app.app_context():
    if not User.query.filter_by(username='test').first():
        hashed_password = bcrypt.generate_password_hash('psd').decode('utf-8')
        test_user = User(username='test', password=hashed_password)
        db.session.add(test_user)
        db.session.commit()


# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Find user by username
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful", "token": access_token}), 200

# Protected route
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"message": f"Welcome, {user.username}!"}), 200

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    # Simple chatbot logic
    if "jacket" in user_message.lower():
        reply = "We have a variety of jackets starting at $50. Check them out!"
    elif "help" in user_message.lower():
        reply = "Sure! I can help you find products, check your order status, or answer questions."
    else:
        reply = "I'm sorry, I didn't understand that. Can you rephrase?"
    
    return jsonify({"reply": reply})

# Products route
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    products = Product.query.filter_by(category=category).all()
    product_list = [
        {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock}
        for p in products
    ]
    return jsonify(product_list)




if __name__ == "__main__":
    app.run(debug=True)
