from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
mongo = PyMongo(app)
db = mongo.db

CORS(app)

class Project:
    def __init__(self, title, description, technologies, image, link, github, github2=None, technologies2=None):
        self.title = title
        self.description = description
        self.technologies = technologies
        self.image = image
        self.link = link
        self.github = github
        self.github2 = github2
        self.technologies2 = technologies2

    def to_json(self):
        project_data = {
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies,
            "image": self.image,
            "link": self.link,
            "github": self.github,
            "github2": self.github2
        }
        if self.technologies2:
            project_data["technologies2"] = self.technologies2
        return project_data

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
        technologies2=data('technologies2'),
        image=data['image'],
        link=data['link'],
        github=data['github'],
        github2=data('github2')
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
        "technologies2": data.get('technologies2'),
        "image": data['image'],
        "link": data['link'],
        "github": data['github'],
        "github2": data.get('github2')
    }
    db.projects.update_one({"_id": ObjectId(id)}, {"$set": updated_project})
    return jsonify({"message": "Project updated"})

@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    db.projects.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Project deleted"})

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        msg = Message(
            "New Contact Form Submission",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}"
        mail.send(msg)
        return jsonify({"message": "Email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test-email', methods=['GET'])
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body="This is a test email sent from Flask."
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
