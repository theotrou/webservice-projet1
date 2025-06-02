import React, { useEffect, useState } from 'react';

function MyNotifications() {
  const [availableBooks, setAvailableBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAvailableBooks = async () => {
      const token = localStorage.getItem('jwt_token');

      if (!token) {
        setError("Utilisateur non connecté.");
        setLoading(false);
        return;
      }

      try {
        // Appel à l'endpoint backend pour récupérer les livres disponibles (notifications)
        const response = await fetch('http://localhost:5009/api/notifications/me', {
          headers: {
            'Authorization': `Bearer ${token}` // Inclure le token JWT
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Erreur lors de la récupération des notifications: ${response.status}`);
        }

        const data = await response.json();
        setAvailableBooks(data);
        setLoading(false);

      } catch (err) {
        console.error("Erreur lors du chargement des notifications:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchAvailableBooks();
  }, []); // Le tableau vide assure que cet effet ne s'exécute qu'une fois au montage

  if (loading) {
    return <div>Chargement des notifications...</div>;
  }

  if (error) {
    return <div>Erreur: {error}</div>;
  }

  return (
    <div>
      <h1>Livres Disponibles à Récupérer (Notifications)</h1>
      {availableBooks.length === 0 ? (
        <p>Aucun livre n'est actuellement disponible à récupérer.</p>
      ) : (
        <ul>
          {availableBooks.map(book => (
            <li key={book.id}>
              {book.title} par {book.author} ({book.published_at ? new Date(book.published_at).getFullYear() : 'N/A'})
              {/* Vous pourriez ajouter un bouton ici pour emprunter le livre directement si désiré */}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MyNotifications;
