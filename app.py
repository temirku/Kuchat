from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kuchat_secret_key_777'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuchat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# База данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # В реальном проекте нужен хеш
    avatar = db.Column(db.Text, nullable=True) # Фото как текст (base64)
    bio = db.Column(db.String(120), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80))
    content = db.Column(db.Text)

# Создаем базу при запуске
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# API: Регистрация
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Логин занят'})
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True})

# API: Вход
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({'success': True, 'username': user.username, 'avatar': user.avatar})
    return jsonify({'success': False})

# API: Обновление профиля (фото и имя)
@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    user = User.query.filter_by(username=data['old_username']).first()
    if user:
        user.username = data['new_username']
        if data.get('avatar'):
            user.avatar = data['avatar']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

# API: Поиск
@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    users = User.query.filter(User.username.contains(query)).all()
    results = [{'username': u.username, 'avatar': u.avatar} for u in users]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


