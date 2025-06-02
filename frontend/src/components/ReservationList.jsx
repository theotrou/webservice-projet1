import React from "react";
import './ReservationList.css';

const ReservationList = ({ reservations }) => {
  return (
    <div className="grid">
      <p>Mes Réservations</p>
      <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Livre</th>
            <th>Statut</th>
            <th>Réservé le</th>
          </tr>
        </thead>
        <tbody>
          {reservations.map(res => (
            <tr key={res.id}>
              <td>{res.id}</td>
              <td>{res.book_id}</td>
              <td>{res.notified ? "📢 Disponible" : "⏳ En attente"}</td>
              <td>{new Date(res.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ReservationList;
