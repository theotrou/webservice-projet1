import React from "react";
import './BookList.css';

const BookList = ({ books, onReserve }) => {
  return (
    <div className="grid">
      <p>Liste de livres empruntés</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Auteur</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {books.map(book => (
            <tr key={book.id}>
              <td>{book.id}</td>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>
                <button onClick={() => onReserve(book.id)}>Réserver</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BookList;
