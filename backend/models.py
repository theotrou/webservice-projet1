from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class StudentBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)

    student = relationship("Student", back_populates="student_books")
    book = relationship("Book", back_populates="student_books")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_at = db.Column(db.DateTime)

    student_books = relationship("StudentBook", back_populates="book", cascade="all, delete-orphan")
    borrowers = relationship("Student", secondary="student_book", viewonly=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime)

    student_books = relationship("StudentBook", back_populates="student", cascade="all, delete-orphan")
    borrowed_books = relationship("Book", secondary="student_book", viewonly=True)

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    position = db.Column(db.Integer, nullable=False)
    notified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("Student", backref="reservations")
    book = relationship("Book", backref="reservations")



class Borrowing(db.Model):
    __tablename__ = "borrowings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    borrowed_at = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = relationship("Student", backref="borrowings")
    book = relationship("Book", backref="borrowings")
