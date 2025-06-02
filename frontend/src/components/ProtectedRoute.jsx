import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  // Vérifier si le token JWT existe dans localStorage
  const token = localStorage.getItem('jwt_token');

  if (!token) {
    // Si aucun token n'est trouvé, rediriger vers la page de login
    return <Navigate to="/login" replace />;
  }

  // Si un token est trouvé, afficher le composant enfant (la page demandée)
  return children;
}

export default ProtectedRoute; 