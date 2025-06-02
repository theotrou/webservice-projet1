import React, { useEffect, useState } from 'react';

function MyReservations() {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMyReservations = async () => {
      const token = localStorage.getItem('jwt_token');
      const userId = localStorage.getItem('user_id');

      if (!token || !userId) {
        setError("Utilisateur non connecté ou ID utilisateur manquant.");
        setLoading(false);
        return;
      }

      try {
        // Appel à l'endpoint backend pour récupérer les réservations de l'utilisateur
        const response = await fetch(`http://localhost:5009/api/reservations/me?user_id=${userId}`, {
          headers: {
            'Authorization': `Bearer ${token}` // Inclure le token JWT
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Erreur lors de la récupération des réservations: ${response.status}`);
        }

        const data = await response.json();
        setReservations(data);
        setLoading(false);

      } catch (err) {
        console.error("Erreur lors du chargement des réservations:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchMyReservations();
  }, []); // Le tableau vide assure que cet effet ne s'exécute qu'une fois au montage

  if (loading) {
    return <div>Chargement de vos réservations...</div>;
  }

  if (error) {
    return <div>Erreur: {error}</div>;
  }

  return (
    <div>
      <h1>Mes Réservations</h1>
      {reservations.length === 0 ? (
        <p>Vous n'avez aucune réservation en cours.</p>
      ) : (
        <ul>
          {reservations.map(reservation => (
            <li key={reservation.id}>
              Livre ID: {reservation.book_id} - 
              Position: {reservation.position} - 
              Statut: {reservation.notified ? 'Disponible (Notifié)' : 'En attente'}
               (Réservé le: {new Date(reservation.created_at).toLocaleDateString()})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MyReservations;
