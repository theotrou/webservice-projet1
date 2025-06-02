import React from "react";
import './LateBorrowings.css';

const LateBorrowings = ({ borrowings }) => {
  return (
    <div className="grid">
      <p>📛 Emprunts en retard</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Livre</th>
            <th>Emprunté le</th>
            <th>Jours de retard</th>
          </tr>
        </thead>
        <tbody>
          {borrowings.map((item) => {
            const borrowedAt = new Date(item.borrowed_at);
            const daysLate = Math.floor((Date.now() - borrowedAt) / (1000 * 60 * 60 * 24)) - 14;

            return (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.book_id}</td>
                <td>{borrowedAt.toLocaleDateString()}</td>
                <td>{daysLate}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default LateBorrowings;
