from flask import Blueprint, jsonify
from models import Book, Borrowing
from sqlalchemy import not_

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/api/notifications/me", methods=["GET"])
def get_available_books():
    # Trouver les IDs des livres actuellement empruntés
    borrowed_book_ids = [b.book_id for b in Borrowing.query.filter_by(returned_at=None).all()]

    # Trouver les livres dont l'ID n'est PAS dans la liste des IDs empruntés
    available_books = Book.query.filter(not_(Book.id.in_(borrowed_book_ids))).all()

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "published_at": book.published_at.strftime('%Y-%m-%d') if book.published_at else None
        }
        for book in available_books
    ]) 