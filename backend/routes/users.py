from flask import Blueprint, request, jsonify
from models import db, Student
from datetime import datetime

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