from flask import Blueprint, request, jsonify
from models import db, Borrowing, Reservation
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
        db.session.commit() # Assure-toi que le commit de retour est toujours là
        return jsonify({
            "message": f"Livre pour l'emprunt {borrowing_id} rendu avec succès. Aucun réservataire en attente."
        }), 200
