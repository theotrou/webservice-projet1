import React from "react";
import './Notifications.css';

const Notifications = ({ notifications }) => {
  if (notifications.length === 0) {
    return <p>Aucune notification pour le moment.</p>;
  }

  return (
    <div className="grid">
      <p>📢 Notifications – Livres disponibles</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Livre</th>
            <th>Date de notification</th>
          </tr>
        </thead>
        <tbody>
          {notifications.map((n) => (
            <tr key={n.id}>
              <td>{n.id}</td>
              <td>{n.book_id}</td>
              <td>{new Date(n.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Notifications;
