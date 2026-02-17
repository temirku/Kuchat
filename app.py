from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuchat.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80))
    content = db.Column(db.Text) # Текст сообщения
    file_data = db.Column(db.Text, nullable=True) # Фото или Голосовое (base64)
    msg_type = db.Column(db.String(20), default='text') # text, photo, audio

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    new_msg = Message(
        sender=data.get('sender', 'Ахмет'),
        content=data.get('content', ''),
        file_data=data.get('file_data'),
        msg_type=data.get('msg_type', 'text')
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({'status': 'sent'})

@app.route('/get_messages')
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        'sender': m.sender,
        'content': m.content,
        'file_data': m.file_data,
        'msg_type': m.msg_type
    } for m in messages])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


