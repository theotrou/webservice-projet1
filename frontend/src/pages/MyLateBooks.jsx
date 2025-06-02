import React, { useEffect, useState } from 'react';

function MyLateBooks() {
  const [lateBorrowings, setLateBorrowings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLateBorrowings = async () => {
      const token = localStorage.getItem('jwt_token');
      const userId = localStorage.getItem('user_id');

      if (!token || !userId) {
        setError("Utilisateur non connecté ou ID utilisateur manquant.");
        setLoading(false);
        return;
      }

      try {
        // Appel à l'endpoint backend pour récupérer les emprunts en retard de l'utilisateur
        const response = await fetch(`http://localhost:5009/api/borrowings/late?user_id=${userId}`, {
          headers: {
            'Authorization': `Bearer ${token}` // Inclure le token JWT
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Erreur lors de la récupération des retards: ${response.status}`);
        }

        const data = await response.json();
        setLateBorrowings(data);
        setLoading(false);

      } catch (err) {
        console.error("Erreur lors du chargement des retards:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLateBorrowings();
  }, []); // Le tableau vide assure que cet effet ne s'exécute qu'une fois au montage

  if (loading) {
    return <div>Chargement de vos retards...</div>;
  }

  if (error) {
    return <div>Erreur: {error}</div>;
  }

  return (
    <div>
      <h1>Mes Retards</h1>
      {lateBorrowings.length === 0 ? (
        <p>Vous n'avez aucun emprunt en retard.</p>
      ) : (
        <ul>
          {lateBorrowings.map(borrowing => (
            <li key={borrowing.id}>
              Emprunt ID: {borrowing.id} - Livre ID: {borrowing.book_id} - 
              Emprunté le: {new Date(borrowing.borrowed_at).toLocaleDateString()} 
              {/* Vous pourriez ajouter plus d'infos sur le livre ici si l'endpoint backend les retournait */}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MyLateBooks;
