from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets

# models
from models.user import User, AllowedEmail, AccessToken
from models.conn import db

auth_bp = Blueprint("auth", __name__, url_prefix='/auth')


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    #validation
    required_fields = ['username', 'password', 'firstName', 'lastName', 'email']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"Error": f"{field} is required."}), 400
    
    username = data["username"].strip().lower()
    password = data["password"]
    email = data["email"].strip().lower()
    allowed_emails = AllowedEmail.get_or_none(AllowedEmail.email == email)

    #check if email is valid
    if not allowed_emails:
        return jsonify({"error": "Email not Authorized"}), 403
    
    #check if the user already exists
    if User.select().where((User.username == username) | (User.email == email)).exists():
        return jsonify({"error": "Username or email already exists"}), 409

    try:
        with db.atomic(): # db.atomic() will automatically rollback if ever there's an error happened.
            user = User.create(
                username = username,
                hashed_password = generate_password_hash(password),
                firstName = data["firstName"],
                lastName = data["lastName"],
                email = email,
                role = allowed_emails.assigned_role,
                email_verified = False,
                is_active = False,
                last_login = None
                )

            import hashlib
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            
            AccessToken.create(
                user=user,
                token_hash=token_hash,
                token_type="email_verification",
                expires_at=datetime.now() + timedelta(hours=24),
                used_at=None
            )
            
            verificiation_link = f"http://localhost:5000/auth/verify-email?token={raw_token}"
            print(verificiation_link)
        
        return jsonify({
            "message": "User registered successfully", 
            "user_id": user.user_id}), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500        


@auth_bp.route("/users", methods=["GET"])
def get_users():
    users = User.select()
    
    if not users:
        return jsonify({"message": "No users found!"})
    
    return jsonify([{
        "username": u.username,
        "firstName": u.firstName,
        "lastName": u.lastName,
        "email": u.email,
        "role": u.role
    } for u in users])