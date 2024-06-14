from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import Config  # Importa la clase Config desde config.py
import os

app = Flask(__name__)
app.config.from_object(Config)  

mongo = PyMongo(app)
db = mongo.db

# Define the Project schema
class Project:
    def __init__(self, title, description, technologies, image, link, github):
        self.title = title
        self.description = description
        self.technologies = technologies
        self.image = image
        self.link = link
        self.github = github

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies,
            "image": self.image,
            "link": self.link,
            "github": self.github
        }

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = db.projects.find()
    result = []
    for project in projects:
        project['_id'] = str(project['_id'])
        result.append(project)
    return jsonify(result)

@app.route('/projects/<id>', methods=['GET'])
def get_project(id):
    project = db.projects.find_one({"_id": ObjectId(id)})
    if project:
        project['_id'] = str(project['_id'])
        return jsonify(project)
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    new_project = Project(
        title=data['title'],
        description=data['description'],
        technologies=data['technologies'],
        image=data['image'],
        link=data['link'],
        github=data['github']
    )
    project_id = db.projects.insert_one(new_project.to_json()).inserted_id
    return jsonify({"_id": str(project_id)})

@app.route('/projects/<id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    updated_project = {
        "title": data['title'],
        "description": data['description'],
        "technologies": data['technologies'],
        "image": data['image'],
        "link": data['link'],
        "github": data['github']
    }
    db.projects.update_one({"_id": ObjectId(id)}, {"$set": updated_project})
    return jsonify({"message": "Project updated"})

@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    db.projects.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Project deleted"})

if __name__ == '__main__':
    app.run(debug=True)
