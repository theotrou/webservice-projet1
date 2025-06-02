from flask import Blueprint, request, jsonify
from models import db, Reservation, Borrowing, Book, Student
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

reservations_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")

@reservations_bp.route("/<int:book_id>", methods=["POST"])
@jwt_required()
def reserve_book(book_id):
    current_user_id = get_jwt_identity()

    existing_reservation = Reservation.query.filter_by(user_id=current_user_id, book_id=book_id, notified=False).first()
    if existing_reservation:
        return jsonify({"error": "Vous avez déjà une réservation en cours pour ce livre.", "reservation_id": existing_reservation.id}), 409

    # Vérifie que le livre est déjà emprunté
    borrowing = Borrowing.query.filter_by(book_id=book_id, returned_at=None).first()
    if not borrowing:
        return jsonify({"error": "Ce livre est disponible"}), 400

    # File FIFO
    count = Reservation.query.filter_by(book_id=book_id).count()
    position = count + 1

    new_reservation = Reservation(
        user_id=current_user_id,
        book_id=book_id,
        position=position,
        notified=False
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Réservation créée", "position": position}), 201

@reservations_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_reservations():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.created_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "book_id": r.book_id,
            "position": r.position,
            "notified": r.notified,
            "created_at": r.created_at.isoformat()
        }
        for r in reservations
    ])

@reservations_bp.route("/book/<int:book_id>", methods=["GET"])
@jwt_required()
def get_book_reservations(book_id):
    reservations = Reservation.query.filter_by(book_id=book_id).order_by(Reservation.position.asc()).all()

    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "book_id": r.book_id,
            "position": r.position,
            "notified": r.notified,
            "created_at": r.created_at.isoformat()
        }
        for r in reservations
    ])
