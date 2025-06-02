from flask import Blueprint, request, jsonify
from models import db, Borrowing
from datetime import datetime

borrowings_bp = Blueprint("borrowings", __name__)

@borrowings_bp.route("/api/borrowings/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    borrowing = Borrowing(
        user_id=user_id,
        book_id=book_id,
        borrowed_at=datetime.utcnow(),
        returned_at=None
    )
    db.session.add(borrowing)
    db.session.commit()
    return jsonify({"message": f"Livre {book_id} emprunté par utilisateur {user_id}"}), 201

@borrowings_bp.route("/api/borrowings/status/<int:book_id>", methods=["GET"])
def borrowing_status(book_id):
    borrowing = Borrowing.query.filter_by(book_id=book_id, returned_at=None).first()
    if borrowing:
        return jsonify({
            "borrowed": True,
            "borrowing_id": borrowing.id,
            "user_id": borrowing.user_id,
            "borrowed_at": borrowing.borrowed_at.isoformat()
        })
    else:
        return jsonify({"borrowed": False})

@borrowings_bp.route("/api/borrowings/<int:borrowing_id>/return", methods=["PUT"])
def return_book(borrowing_id):
    borrowing = Borrowing.query.get(borrowing_id)

    if not borrowing:
        return jsonify({"error": "Emprunt non trouvé"}), 404

    if borrowing.returned_at is not None:
        return jsonify({"error": "Livre déjà rendu"}), 400

    borrowing.returned_at = datetime.utcnow()
    db.session.commit()

    # TODO: Ajouter la logique d'attribution au prochain en file et notification ici

    return jsonify({"message": f"Livre pour l'emprunt {borrowing_id} rendu avec succès"}), 200
