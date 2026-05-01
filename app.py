# from flask_mail import Mail, Message
from flask import Flask, session, request, redirect, render_template,jsonify, Blueprint
from werkzeug.security import generate_password_hash
from datetime import datetime,timedelta
import secrets

# models
from models.user import User, AllowedEmail
from models.conn import db

# routes
from routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect("/health")

@app.route("/admin/add_user", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data = request.get_json()
        required_fields = ['email','assigned_role']

        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"Error": f"{field} is required"}), 400

        email = data["email"].strip().lower()
        assigned_role = data["assigned_role"].strip().lower()
        
        try:
            with db.atomic():
                AllowedEmail.create(
                    email=email,
                    assigned_role=assigned_role
                )
                
                return jsonify({
                    "Message": "Added Successfully!",
                    "Reponse": 200
                    }), 201
        except Exception as e:
            return jsonify({"Error": "Internal server Error"}), 500
    
    allowed_emails = AllowedEmail.select()
    return jsonify([
        {
            "email": item.email,
            "assigned_role": item.assigned_role
        } for item in allowed_emails])

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "message": "Welcome to Automatik API!",
        "status": "healthy",
        }), 200

if __name__ == "__main__":
    app.run(debug=True)
