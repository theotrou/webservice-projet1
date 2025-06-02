import React, { useEffect, useState } from 'react';

function BooksPage() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fonction pour gérer la réservation d'un livre
  const handleReserve = async (bookId) => {
    const token = localStorage.getItem('jwt_token');
    const userId = localStorage.getItem('user_id'); // Récupérer l'user_id

    if (!token || !userId) {
      // Gérer le cas où l'utilisateur n'est pas connecté
      console.error("Utilisateur non connecté ou ID utilisateur manquant.");
      // Rediriger vers la page de login
      // navigate('/login'); // Si vous avez accès à navigate ici
      return;
    }

    try {
      const response = await fetch(`http://localhost:5009/api/reservations/${bookId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ user_id: parseInt(userId) }) // Envoyer l'user_id dans le corps
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Erreur lors de la réservation: ${response.status}`);
      }

      const result = await response.json();
      console.log("Réservation réussie:", result);
      alert("Réservation réussie ! Position dans la file : " + result.position); // Afficher un message de succès

      // Optionnel: rafraîchir la liste des livres et leur statut après une réservation réussie
      // fetchBooksAndStatus(); 

    } catch (err) {
      console.error("Erreur lors de la réservation:", err);
      alert("Erreur lors de la réservation: " + err.message); // Afficher un message d'erreur
    }
  };

  useEffect(() => {
    const fetchBooksAndStatus = async () => {
      try {
        // Récupérer la liste de tous les livres
        const booksResponse = await fetch('http://localhost:5009/books');
        if (!booksResponse.ok) {
          throw new Error(`Erreur lors de la récupération des livres: ${booksResponse.status}`);
        }
        const booksData = await booksResponse.json();

        // Pour chaque livre, vérifier son statut d'emprunt
        const booksWithStatus = await Promise.all(booksData.map(async (book) => {
          // Récupérer le token JWT depuis localStorage
          const token = localStorage.getItem('jwt_token');
          
          const statusResponse = await fetch(`http://localhost:5009/api/borrowings/status/${book.id}`, {
            headers: {
              'Authorization': `Bearer ${token}` // <-- Ajouter l'en-tête Authorization
            }
          });

          if (!statusResponse.ok) {
             // Si l'appel échoue (par exemple 401 Unauthorized), gérer l'erreur
             console.error(`Erreur statut livre ${book.id}: ${statusResponse.status}`);
             // On pourrait rediriger vers la page de login si c'est une 401
             // if (statusResponse.status === 401) { navigate('/login'); }
             // Retourner le livre avec un statut par défaut ou une indication d'erreur de statut
             return { ...book, borrowed: false, status_error: true }; // Ajouter un indicateur d'erreur
           }
          const statusData = await statusResponse.json();
          return { ...book, ...statusData };
        }));

        setBooks(booksWithStatus);
        setLoading(false);

      } catch (err) {
        console.error("Erreur lors du chargement des données:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchBooksAndStatus();
  }, []);

  if (loading) {
    return <div>Chargement des livres...</div>;
  }

  if (error) {
    return <div>Erreur: {error}</div>;
  }

  return (
    <div>
      <h1>Liste des Livres</h1>
      <ul>
        {books.map(book => (
          <li key={book.id}>
            {book.title} par {book.author} ({book.published_at ? new Date(book.published_at).getFullYear() : 'N/A'})
            - Statut: {
               book.status_error ? 'Statut inconnu (erreur de récupération)' :
               book.borrowed ? `Emprunté par utilisateur ${book.user_id || 'N/A'} (jusqu'au ${book.borrowed_at ? new Date(new Date(book.borrowed_at).getTime() + 14 * 24 * 60 * 60 * 1000).toLocaleDateString() : 'date inconnue'})` : 'Disponible'
            }
            {book.borrowed && (
              <button onClick={() => handleReserve(book.id)} disabled={false}>
                Réserver
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BooksPage; 