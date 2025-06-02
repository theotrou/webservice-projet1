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
            "user_id": borrowing.user_id,
            "borrowed_at": borrowing.borrowed_at.isoformat()
        })
    else:
        return jsonify({"borrowed": False})
