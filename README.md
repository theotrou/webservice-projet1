# Bibliothèque ESME - Application de Gestion de Bibliothèque

Une application moderne de gestion de bibliothèque universitaire permettant aux étudiants d'emprunter et réserver des livres en ligne. L'application gère automatiquement les listes d'attente et les notifications.

## 🌐 URLs des services

- **Frontend** : [http://localhost:5173](http://localhost:5173)
- **Backend API** : [http://localhost:5009](http://localhost:5009)

> **Note :** Le backend n'est pas accessible directement sur le port 5009. Utilisez les routes API listées ci-dessous.

## 💾 Base de données PostgreSQL

- **Hôte** : localhost
- **Port** : 5432
- **Utilisateur** : myuser
- **Mot de passe** : mot_de_passe
- **Base** : esme_inge

## 🌟 Fonctionnalités principales

- **Gestion des emprunts** : Emprunt et retour de livres avec suivi automatique des retards
- **Système de réservation** : File d'attente FIFO pour les livres indisponibles
- **Notifications** : Alertes automatiques quand un livre réservé devient disponible
- **Sécurité** : Authentification JWT pour protéger les routes sensibles

## 🚀 Installation

```bash
# Démarrer l'application
docker-compose up --build

# Arrêter l'application
docker-compose down
```

## 👥 Comptes de test

| Email | ID |
|-------|----|
| `dilshan@example.com` | 1 |
| `paul@example.com` | 2 |

## 📚 Guide d'utilisation de l'API

### 1. Authentification
```http
POST /api/users/login
{
  "email": "user1@esme.fr"
}
```
> Conservez le token JWT reçu pour les requêtes suivantes

### 2. Gestion des livres
```http
# Lister tous les livres disponibles
GET /books

# Ajouter un nouveau livre
POST /books
{
  "title": "Titre du livre",
  "author": "Nom de l'auteur"
}

# Voir les détails d'un livre
GET /books/<id>
```

### 3. Emprunts et retours
```http
# Emprunter un livre
POST /api/borrowings/<id>

# Retourner un livre
PUT /api/borrowings/<id>/return

# Vérifier les retards
GET /api/borrowings/late
```

### 4. Réservations
```http
# Réserver un livre indisponible
POST /api/reservations/<id>

# Voir mes réservations
GET /api/reservations/me

# Voir la liste d'attente d'un livre
GET /api/reservations/book/<id>
```

### 5. Notifications
```http
# Voir les livres disponibles
GET /api/notifications/me
```

## 🔒 Sécurité

- Toutes les routes (sauf login) nécessitent un token JWT
- Ajoutez l'en-tête `Authorization: Bearer <token>` à vos requêtes
- Les utilisateurs ne peuvent voir que leurs propres données

## 💡 Exemple de workflow

1. Un étudiant se connecte avec son email
2. Il consulte la liste des livres disponibles
3. Si le livre est disponible, il peut l'emprunter
4. Si le livre est emprunté, il peut le réserver
5. Quand le livre est rendu, le premier de la liste d'attente est notifié
6. L'étudiant peut voir ses retards éventuels

## 🛠 Technologies utilisées

- **Backend** : Flask (Python)
- **Base de données** : PostgreSQL
- **Authentification** : JWT
- **Conteneurisation** : Docker