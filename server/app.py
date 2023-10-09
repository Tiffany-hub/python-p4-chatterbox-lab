from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Define a custom CORS function
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    messages_serialized = [message.serialize() for message in messages]
    response = jsonify(messages_serialized)
    return add_cors_headers(response)

@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = Message.query.get_or_404(id)
    response = jsonify(message.serialize())
    return add_cors_headers(response)

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    if body and username:
        message = Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        response = jsonify(message.serialize()), 201
    else:
        response = jsonify({'error': 'Both body and username are required'}), 400

    return add_cors_headers(response)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    new_body = request.json.get('body')

    if new_body:
        message.body = new_body
        db.session.commit()
        response = jsonify(message.serialize())
    else:
        response = jsonify({'error': 'No data provided for update'}), 400

    return add_cors_headers(response)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    response = jsonify({'message': 'Message deleted successfully'})
    return add_cors_headers(response)

if __name__ == '__main__':
    app.run(port=5555)
