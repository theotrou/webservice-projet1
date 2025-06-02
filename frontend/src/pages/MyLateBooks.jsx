import LateBorrowings from '../components/LateBorrowings/LateBorrowings.jsx';
import { useEffect, useState } from 'react';

function MyLateBooks() {
  const [lateBooks, setLateBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5009/api/borrowings/late')
      .then(res => res.json())
      .then(data => setLateBooks(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {loading ? <p>Chargement des retards...</p> : <LateBorrowings borrowings={lateBooks} />}
    </div>
  );
}

export default MyLateBooks;
