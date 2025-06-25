#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

from flask_cors import CORS
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)


api.add_resource(PlantByID, '/plants/<int:id>')


@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = db.session.get(Plant, id)
    if plant:
        return jsonify(plant.to_dict()), 200
    return jsonify({"error": "Plant not found"}), 404

@app.route("/plants/<int:id>", methods=["PATCH"])
def update_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(plant, key, value)

    db.session.commit()
    return jsonify(plant.to_dict()), 200

@app.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    db.session.delete(plant)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)