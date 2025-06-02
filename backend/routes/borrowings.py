from flask import Blueprint, jsonify
from models import db, Borrowing
from datetime import datetime

borrowings_bp = Blueprint("borrowings", __name__)

@borrowings_bp.route("/api/test/emprunt", methods=["POST"])
def test_emprunt():
    # Emprunt du livre 1 par l'étudiant 1
    emprunt = Borrowing(
        user_id=1,
        book_id=1,
        borrowed_at=datetime.utcnow(),
        returned_at=None
    )

    db.session.add(emprunt)
    db.session.commit()

    return jsonify({"message": "Livre 1 emprunté par étudiant 1"}), 201
