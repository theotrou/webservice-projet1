import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch('http://localhost:5009/api/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || `Erreur de login: ${response.status}`);
      }

      const data = await response.json();
      // Stocker le token et l'user_id (par exemple, dans localStorage)
      localStorage.setItem('jwt_token', data.access_token);
      localStorage.setItem('user_id', data.user_id);
      
      // Rediriger l'utilisateur après le login
      navigate('/'); // Rediriger vers la page d'accueil

    } catch (err) {
      console.error("Erreur lors du login:", err);
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Connexion</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Se connecter</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
}

export default LoginPage; 