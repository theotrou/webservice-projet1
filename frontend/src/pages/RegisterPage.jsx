import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch('http://localhost:5009/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          email,
          first_name: firstName,
          last_name: lastName,
          birth_date: birthDate || null // Envoyer null si la date est vide
         }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Erreur d'inscription: ${response.status}`);
      }

      const data = await response.json();
      console.log("Utilisateur créé:", data);
      setSuccess(true);
      // Optionnel: Rediriger vers la page de login après succès
      // navigate('/login');

    } catch (err) {
      console.error("Erreur lors de l'inscription:", err);
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Créer un Compte</h1>
      <form onSubmit={handleRegister}>
        <div>
          <label htmlFor="email">Email:</label>
          <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="firstName">Prénom:</label>
          <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="lastName">Nom:</label>
          <input type="text" id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="birthDate">Date de Naissance:</label>
          <input type="date" id="birthDate" value={birthDate} onChange={(e) => setBirthDate(e.target.value)} />
        </div>
        <button type="submit">Créer le Compte</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>Compte créé avec succès ! Vous pouvez maintenant vous connecter.</p>}
      </form>
      <p><button onClick={() => navigate('/login')}>Aller à la page de Connexion</button></p>
    </div>
  );
}

export default RegisterPage; 