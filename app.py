from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from config import Config
import os
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
mongo = PyMongo(app)
db = mongo.db

CORS(app)  # Habilita CORS para toda la aplicación


class Project:
    def __init__(self, title, description, technologies, image, link, github, technologies2):
        self.title = title
        self.description = description
        self.technologies = technologies
        self.image = image
        self.link = link
        self.github = github
        self.technologies2 = technologies2

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies,
            "image": self.image,
            "link": self.link,
            "github": self.github,
            "technologies2": self.technologies2
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
        technologies2=data['technologies2'],
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
        "technologies2": data['technologies2'],
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

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    subject = "Mensaje de contacto" 
    sender = app.config['MAIL_USERNAME']  
    recipients = [data['email']] 

    # Crea el mensaje de correo
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = f"Nombre: {data['name']}\nEmail: {data['email']}\n\nMensaje:\n{data['message']}"

    try:
        mail.send(msg)  # Envía el correo
        return jsonify({"message": "Email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test-email', methods=['GET'])
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],  # Enviando a ti mismo para probar
            body="This is a test email sent from Flask."
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
