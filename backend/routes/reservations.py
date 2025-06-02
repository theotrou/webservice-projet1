from flask import Blueprint, request, jsonify
from models import db, Reservation, Borrowing

reservations_bp = Blueprint("reservations", __name__)

@reservations_bp.route("/api/reservations/<int:book_id>", methods=["POST"])
def reserve_book(book_id):
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    # Vérifie que le livre est déjà emprunté
    borrowing = Borrowing.query.filter_by(book_id=book_id, returned_at=None).first()
    if not borrowing:
        return jsonify({"error": "Ce livre est disponible"}), 400

    # File FIFO
    count = Reservation.query.filter_by(book_id=book_id).count()
    position = count + 1

    new_reservation = Reservation(
        user_id=user_id,
        book_id=book_id,
        position=position,
        notified=False
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Réservation créée", "position": position}), 201
