import ReservationList from '../components/ReservationList';
import { useState, useEffect } from 'react';

function MyReservations() {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5009/api/reservations/me')
      .then(res => res.json())
      .then(data => setReservations(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {loading ? <p>Chargement...</p> : <ReservationList reservations={reservations} />}
    </div>
  );
}

export default MyReservations;
