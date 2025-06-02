from flask import Blueprint, request, jsonify
from models import db, Borrowing, Reservation, Book, Student
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

borrowings_bp = Blueprint("borrowings", __name__)

@borrowings_bp.route("/api/borrowings/<int:book_id>", methods=["POST"])
@jwt_required()
def borrow_book(book_id):
    current_user_id = get_jwt_identity()
    # user_id = request.json.get("user_id") # <-- Cette ligne ne sera plus nécessaire
    # if not user_id:
    #     return jsonify({"error": "user_id requis"}), 400

    borrowing = Borrowing(
        user_id=current_user_id,
        book_id=book_id,
        borrowed_at=datetime.utcnow(),
        returned_at=None
    )
    db.session.add(borrowing)
    db.session.commit()
    return jsonify({"message": f"Livre {book_id} emprunté par utilisateur {current_user_id}"}), 201

@borrowings_bp.route("/api/borrowings/status/<int:book_id>", methods=["GET"])
@jwt_required()
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
@jwt_required()
def return_book(borrowing_id):
    borrowing = Borrowing.query.get(borrowing_id)

    if not borrowing:
        return jsonify({"error": "Emprunt non trouvé"}), 404

    if borrowing.returned_at is not None:
        return jsonify({"error": "Livre déjà rendu"}), 400

    # --- Marquer l'emprunt comme rendu ---
    borrowing.returned_at = datetime.utcnow()
    db.session.commit() # Commit the return first, so the book is technically available

    # --- Logique d'attribution au prochain en file et notification ---
    # Trouver la première réservation pour ce livre (position 1, non notifiée)
    next_reservation = Reservation.query.filter_by(
        book_id=borrowing.book_id,
        position=1, # La première personne en file
        notified=False # Pas encore notifiée
    ).first()

    if next_reservation:
        # Notifier la première personne
        next_reservation.notified = True

        # Créer un nouvel emprunt pour la personne notifiée (attribution automatique)
        new_borrowing = Borrowing(
            user_id=next_reservation.user_id,
            book_id=next_reservation.book_id,
            borrowed_at=datetime.utcnow(),
            returned_at=None # Le nouveau prêt est actif
        )
        db.session.add(new_borrowing)

        # Décrémenter la position des autres réservations pour ce livre
        # On récupère toutes les réservations pour ce livre dont la position est supérieure à 1
        remaining_reservations = Reservation.query.filter(
            Reservation.book_id == borrowing.book_id,
            Reservation.position > 1,
            Reservation.notified == False # Seulement celles qui attendent toujours
        ).order_by(Reservation.position.asc()).all()

        for res in remaining_reservations:
            res.position -= 1

        # On peut aussi supprimer la réservation qui vient d'être notifiée/attribuée,
        # car elle n'est plus en attente dans la file.
        # db.session.delete(next_reservation) # Optionnel, selon si tu veux garder un historique des réservations notifiées/servies

        # Committer les changements (notification, nouvel emprunt, positions)
        db.session.commit()

        return jsonify({
            "message": f"Livre pour l'emprunt {borrowing_id} rendu. Attribué à l'utilisateur {next_reservation.user_id} via réservation {next_reservation.id}.",
            "next_user_notified": next_reservation.user_id
        }), 200
    else:
        # Aucun réservataire en attente
        db.session.commit() # Assure-toi que le commit du retour est toujours là
        return jsonify({
            "message": f"Livre pour l'emprunt {borrowing_id} rendu avec succès. Aucun réservataire en attente."
        }), 200

# Endpoint pour lister les emprunts en retard
@borrowings_bp.route("/api/borrowings/late", methods=["GET"])
@jwt_required()
def get_late_borrowings():
    # Calculer la date il y a 14 jours
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)

    # Commencer la requête pour trouver les emprunts en retard non rendus
    query = Borrowing.query.filter(
        Borrowing.returned_at.is_(None), # Emprunt non rendu
        Borrowing.borrowed_at < fourteen_days_ago # Emprunté il y a plus de 14 jours
    )

    # --- Utiliser get_jwt_identity() si aucun user_id n\'est fourni en paramètre ---
    requested_user_id = request.args.get("user_id")
    user_id_to_filter = None

    if requested_user_id:
        # Si user_id est fourni dans la requête, l\'utiliser
        try:
            user_id_to_filter = int(requested_user_id)
        except ValueError:
            return jsonify({"error": "user_id doit être un entier"}), 400
    else:
        # Si user_id n\'est pas fourni, utiliser l\'ID de l\'utilisateur authentifié
        current_user_id_str = get_jwt_identity()
        try:
            # Assurez-vous que l\'identité est un entier
            user_id_to_filter = int(current_user_id_str)
        except ValueError:
             return jsonify({"error": "L\'identité JWT n\'est pas un ID utilisateur valide"}), 400

    # Appliquer le filtre par user_id (soit celui de la requête, soit celui du token)
    query = query.filter(Borrowing.user_id == user_id_to_filter)

    # Exécuter la requête filtrée
    late_borrowings = query.all()

    # TODO: Récupérer les infos du livre et de l\'utilisateur si nécessaire pour l\'affichage

    return jsonify([
        {
            "id": b.id,
            "user_id": b.user_id,
            "book_id": b.book_id,
            "borrowed_at": b.borrowed_at.isoformat(),
            "returned_at": b.returned_at.isoformat() if b.returned_at else None
        }
        for b in late_borrowings
    ])
