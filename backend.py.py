from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # To handle Cross-Origin Resource Sharing (CORS)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feastforward.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # provider/volunteer/recipient
    location = db.Column(db.String(100), nullable=False)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    freshness_score = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='available')  # available/picked up/delivered

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=True)

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_requirements = db.Column(db.String(200), nullable=True)
    number_of_people = db.Column(db.Integer, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return "Welcome to FeastForward Backend!"

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        location=data['location']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# Food Donation
@app.route('/food', methods=['POST'])
def post_food():
    data = request.get_json()
    new_food = Food(
        provider_id=data['provider_id'],
        type=data['type'],
        quantity=data['quantity'],
        freshness_score=data.get('freshness_score'),
        location=data['location'],
        status='available'
    )
    db.session.add(new_food)
    db.session.commit()
    return jsonify({"message": "Food posted successfully!"}), 201

# Get All Food Posts
@app.route('/food', methods=['GET'])
def get_food():
    food_posts = Food.query.all()
    output = []
    for food in food_posts:
        food_data = {
            'id': food.id,
            'provider_id': food.provider_id,
            'type': food.type,
            'quantity': food.quantity,
            'freshness_score': food.freshness_score,
            'location': food.location,
            'status': food.status
        }
        output.append(food_data)
    return jsonify({"food_posts": output})

# Volunteer Sign-Up
@app.route('/volunteer', methods=['POST'])
def register_volunteer():
    data = request.get_json()
    new_volunteer = Volunteer(
        user_id=data['user_id'],
        vehicle_type=data.get('vehicle_type')
    )
    db.session.add(new_volunteer)
    db.session.commit()
    return jsonify({"message": "Volunteer registered successfully!"}), 201

# Recipient Request
@app.route('/recipient', methods=['POST'])
def register_recipient():
    data = request.get_json()
    new_recipient = Recipient(
        user_id=data['user_id'],
        food_requirements=data.get('food_requirements'),
        number_of_people=data['number_of_people']
    )
    db.session.add(new_recipient)
    db.session.commit()
    return jsonify({"message": "Recipient registered successfully!"}), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)