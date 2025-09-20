# Documentation de l'API ICARTABLE - User Auth Service

Cette documentation couvre toutes les **mutations GraphQL** disponibles pour le module d'authentification utilisateur ICARTABLE. Elle inclut les paramètres, exemples de requêtes, résultats attendus, erreurs possibles et recommandations pour l'utilisateur.

---

## 🔹 Microservice ICARTABLE

- **Objectif** : Gestion des connexions, sessions et authentification des utilisateurs.
- **Technologies** : Django, MySQL, Graphene-Django, GraphQL JWT.
- **Fonctionnalités principales** :
  - Création et gestion de comptes utilisateurs.
  - Vérification par code envoyé par email.
  - Changement et réinitialisation de mot de passe.
  - Gestion des droits d'administration.
  - Authentification via JWT et rafraîchissement de tokens.

---

## 🔹 Mutations disponibles

### 1. Créer un compte utilisateur
```graphql
mutation {
  createUserLogin(username: "alice", password: "motdepasse", email: "alice@mail.com") {
    userLogin {
      id
      username
      email
    }
  }
}
