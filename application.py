from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task
from database import db
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.post('/api/register')
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], email=data['email'], mobile_number=data['mobile_number'],
                    password=hashed_password, address=data['address'], 
                    latitude=data['latitude'], longitude=data['longitude'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.post('/api/login')
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'email': user.email, 'name': user.name})
        return jsonify({'token': access_token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.get('/api/users')
@jwt_required()
def get_users():
    users = User.query.all()
    output = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(output)

@app.post('/api/tasks')
@jwt_required()
def add_task():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()
    new_task = Task(name=data['name'], date_time=datetime.datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S'),
                    assigned_user_id=data['assigned_user_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'})

@app.get('/api/tasks')
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()
    tasks = Task.query.filter_by(assigned_user_id=user.id).all()
    output = [{'id': task.id, 'name': task.name, 'date_time': task.date_time, 'status': task.status} for task in tasks]
    return jsonify(output)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
