import Notifications from '../components/Notifications/Notifications.jsx';
import { useEffect, useState } from 'react';

function MyNotifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5009/api/notifications/me')
      .then(res => res.json())
      .then(data => setNotifications(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {loading ? <p>Chargement des notifications...</p> : <Notifications notifications={notifications} />}
    </div>
  );
}

export default MyNotifications;
