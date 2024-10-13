from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Ad(db.Model):
    __tablename__ = 'ads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


# Применяем сразу при запуске миграции
@app.before_request
def apply_migrations():
    with app.app_context():
        upgrade()


@app.route('/ads', methods=['POST'])
def create_ad():
    data = request.json
    new_ad = Ad(
        title=data['title'],
        description=data['description'],
        owner=data['owner']
    )
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({"message": "Объявление успешно создано", "ad_id": new_ad.id}), 201


@app.route('/ads/<int:id>', methods=['GET'])
def get_ad(id):
    ad = Ad.query.get_or_404(id)
    return jsonify({
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner': ad.owner
    })


@app.route('/ads/<int:id>', methods=['DELETE'])
def delete_ad(id):
    ad = Ad.query.get_or_404(id)
    db.session.delete(ad)
    db.session.commit()
    return jsonify({"message": "Объявление успешно удалено"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
