#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)

    if animal:
        response_content = f'<ul>ID: {animal.id}</ul>'

        response_content += f'<ul>Name: {animal.name}</ul>'

        response_content += f'<ul>Species: {animal.species}</ul>'

        zookeeper = animal.zookeeper
        enclosure = animal.enclosure

        if zookeeper:
            response_content += f'<ul>Zookeeper: {zookeeper.name}</ul>'

        if enclosure:
            response_content += f'<ul>Enclosure: {enclosure.environment}</ul>'

        response = make_response(response_content)
        response.status_code = 200
        return response
    else:
        return '<p>Animal not found</p>', 404
    
@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    
    if zookeeper:
        response_content = f'<ul>ID: {zookeeper.id}</ul>'
        response_content += f'<ul>Name: {zookeeper.name}</ul>'
        response_content += f'<ul>Birthday: {zookeeper.birthday}</ul>'
        
        animals = zookeeper.animals
        
        if animals:
            for animal in animals:
                response_content += f'<ul>Animal: {animal.name}</ul>'
        
        response = make_response(response_content)
        response.status_code = 200
        return response
    else:
        return '<p>Zookeeper not found</p>', 404
    
@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    
    if enclosure:
        response_content = f'<ul>ID: {enclosure.id}</ul>'
        response_content += f'<ul>Environment: {enclosure.environment}</ul>'
        response_content += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'
        
        animals = enclosure.animals
        
    if animals:
        for animal in animals:
            response_content += f'<ul>Animal: {animal.name}</ul>'
        
        response = make_response(response_content)
        response.status_code = 200
        return response
    else:
        return '<p>Enclosure not found</p>', 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)