#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/baked_goods', methods=['POST'])
def create_bakery():
    print("Received POST request to /baked_goods")

    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            print("Received JSON data json:", data)
        else:
            data = request.form
            print("Received JSON data form:", data)
        
        name = data.get('name')
        print("Extracted name from JSON data:", name)

        if name:
            new_baked_good = BakedGood(name=name)
            db.session.add(new_baked_good)
            db.session.commit()
            print("New bakery added to the database:", new_baked_good)

            # Retrieve the newly created baked good from the database
            new_baked_good = BakedGood.query.filter_by(name=name).first()

            return jsonify({'id': new_baked_good.id, 'name': new_baked_good.name}), 201
        else:
            print("Name is required. Returning error response.")
            return jsonify({'error': 'Name is required'}), 400

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        print("NU")
        data = request.form
        print("NU@")
        if 'name' in data:
            bakery.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Bakery updated successfully'}), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

# Delete Baked Goods Route
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return jsonify({'error': 'Baked good not found'}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({'message': 'Baked good deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)