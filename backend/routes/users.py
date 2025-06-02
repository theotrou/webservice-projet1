from flask import Blueprint, request, jsonify
from models import db, Student
from datetime import datetime

# Importer les fonctions JWT nécessaires
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "first_name", "last_name")):
        return jsonify({"error": "email, first_name et last_name sont requis"}), 400

    birth_date = None
    if "birth_date" in data and data["birth_date"]:
        try:
            birth_date = datetime.strptime(data["birth_date"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Format de date invalide, attendu YYYY-MM-DD"}), 400

    user = Student(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        birth_date=birth_date
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "message": "Utilisateur créé"}), 201

# Endpoint de login (simulation simple par email)
@users_bp.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email: # Pour l'instant, on vérifie juste l'email
        return jsonify({"msg": "Email manquant"}), 400

    # Chercher l'utilisateur par email
    user = Student.query.filter_by(email=email).first()

    # Dans un vrai système, vous vérifieriez aussi le mot de passe ici
    if user: # and user.check_password(password):
        # Créer le token d'accès. L'identité du token est l'ID de l'utilisateur
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Mauvais email ou mot de passe"}), 401 