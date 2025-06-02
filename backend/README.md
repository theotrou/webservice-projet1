# Flask Books API

Ce projet est une API REST simple développée avec Flask pour gérer une collection de livres, utilisant PostgreSQL comme base de données et Docker pour faciliter la gestion des environnements.

## 🌐 URLs des services

- **Frontend** : [http://localhost:5173](http://localhost:5173)

> **Note :** L'API backend n'est pas accessible directement sur le port 5009. Utilisez les routes API listées ci-dessous pour interagir avec le backend.

---

## 🚀 Installation & Exécution

### 📌 Prérequis

**Recommandations d'outils complémentaires :**
- [Postman](https://www.postman.com/downloads/) pour tester les endpoints de l'API.
- [DBeaver](https://dbeaver.io/download/) pour visualiser la base de données.

#### 🖥️ Windows
- Installer [Python](https://www.python.org/downloads/)
- Installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Installer [Make for Windows (GnuWin32)](http://gnuwin32.sourceforge.net/packages/make.htm) ou utiliser [Chocolatey](https://chocolatey.org/install) : `choco install make`
- **Ajouter `make` dans le PATH système** pour pouvoir exécuter les commandes `make` dans un terminal (cmd ou PowerShell)

#### 🐧 Linux / 🍏 macOS
- Vérifier que `python3`, `pip`, `docker`, `docker-compose` et `make` sont installés

### 🏗️ Installation

#### 1️⃣ Cloner le projet
```bash
git clone git@github.com:esperluet/esme_webservice_flask.git
cd esme_webservice_flask
```

#### 2️⃣ Démarrer l'application avec Docker Compose
```bash
docker-compose up --build
```

> **Note :** Pour arrêter l'application :
> ```bash
> docker-compose down
> ```

### 👥 Comptes utilisateurs de test

| Email | Mot de passe | Rôle |
|-------|--------------|------|
| `admin@esme.fr` | `admin123` | Administrateur |
| `user1@esme.fr` | `user123` | Étudiant |
| `user2@esme.fr` | `user123` | Étudiant |

> **Note :** Pour créer un nouveau compte, utilisez l'endpoint `POST /api/users` avec un email et un mot de passe.

---

## 📚 Routes API principales

### 🔐 Authentification
```http
POST /api/users/login
Content-Type: application/json

{
  "email": "user1@esme.fr",
  "password": "user123"
}
```
> **Note :** Ajoutez le token JWT reçu dans l'en-tête `Authorization: Bearer <token>` pour les requêtes suivantes.

### 📖 Gestion des livres
```http
GET /books                    # Liste tous les livres
POST /books                   # Ajoute un livre
GET /books/<book_id>          # Détails d'un livre
PUT /books/<book_id>          # Met à jour un livre
DELETE /books/<book_id>       # Supprime un livre
```

### 📚 Emprunts
```http
POST /api/borrowings/<book_id>           # Emprunte un livre
PUT /api/borrowings/<borrowing_id>/return # Retourne un livre
GET /api/borrowings/late                 # Liste les retards
GET /api/borrowings/status/<book_id>     # Vérifie le statut d'un livre
```

### 📝 Réservations
```http
POST /api/reservations/<book_id>         # Réserve un livre
GET /api/reservations/me                 # Liste mes réservations
GET /api/reservations/book/<book_id>     # Liste les réservations d'un livre
```

### 🔔 Notifications
```http
GET /api/notifications/me                # Liste les livres disponibles
```

---

## 🛠 Commandes utiles

| Commande             | Description                                              |
|----------------------|----------------------------------------------------------|
| `docker-compose up --build` | Construit et démarre les conteneurs Docker        |
| `docker-compose down` | Arrête et supprime les conteneurs                        |
| `docker-compose logs -f` | Affiche les logs en temps réel                    |

---

## 🛠 Technologies utilisées

- **Flask** : Framework web en Python pour la création de l'API REST.
- **PostgreSQL** : Base de données relationnelle pour le stockage des livres.
- **Docker & Docker Compose** : Gestion des environnements et conteneurisation.
- **JWT** : Authentification sécurisée avec JSON Web Tokens.

---

## ❗ Conseils supplémentaires

- Assurez-vous que Docker Desktop est en cours d'exécution avant de lancer les commandes.
- Pour tester les endpoints protégés, n'oubliez pas d'inclure le token JWT dans l'en-tête `Authorization`.
- Les données sont persistantes grâce au volume Docker `postgres_data`.