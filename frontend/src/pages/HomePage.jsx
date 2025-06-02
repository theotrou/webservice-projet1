import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <h1>Bienvenue à la Bibliothèque ESME</h1>
      <p>Ceci est la page d'accueil de l'application.</p>
      
      <h2>Options :</h2>
      <ul>
        <li><Link to="/login">Se Connecter</Link></li>
        <li><Link to="/register">Créer un Compte</Link></li>
        <li><Link to="/books">Liste des Livres</Link></li>
        <li><Link to="/reservations">Mes Réservations</Link></li>
        <li><Link to="/late">Mes Retards</Link></li>
        <li><Link to="/notifications">Notifications (Livres disponibles)</Link></li>
      </ul>

    </div>
  );
}

export default HomePage; 