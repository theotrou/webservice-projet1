from flask import Blueprint, request, jsonify
from models import db, Reservation, Borrowing

reservations_bp = Blueprint("reservations", __name__)

@reservations_bp.route("/api/reservations/<int:book_id>", methods=["POST"])
def reserve_book(book_id):
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    existing_reservation = Reservation.query.filter_by(user_id=user_id, book_id=book_id, notified=False).first()
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
        user_id=user_id,
        book_id=book_id,
        position=position,
        notified=False
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Réservation créée", "position": position}), 201

@reservations_bp.route("/api/reservations/me", methods=["GET"])
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

@reservations_bp.route("/api/reservations/book/<int:book_id>", methods=["GET"])
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

# Endpoint pour consulter les notifications d'un utilisateur
@reservations_bp.route("/api/notifications/me", methods=["GET"])
def get_my_notifications():
    # Pour l'instant, on utilise user_id en paramètre pour les tests
    # TODO: Remplacer par l'extraction du user_id depuis le token JWT
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requis (ou token JWT manquant)"}), 400

    # Récupérer les réservations pour cet utilisateur où notified est True
    notifications = Reservation.query.filter_by(
        user_id=user_id,
        notified=True
    ).order_by(Reservation.created_at.desc()).all() # On peut trier par date de création

    return jsonify([
        {
            "id": n.id,
            "book_id": n.book_id,
            "user_id": n.user_id,
            "position": n.position, # La position au moment de la notification (si pertinent)
            "notified": n.notified,
            "created_at": n.created_at.isoformat()
            # On pourrait aussi ajouter des infos sur le livre ici en joignant les tables si nécessaire
        }
        for n in notifications
    ])
