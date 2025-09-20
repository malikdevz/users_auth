Voici une **documentation complète en Markdown** basée sur le nouveau code que tu as fourni. Elle est structurée pour que quelqu’un puisse utiliser ton API même sans le développeur :

````markdown
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
````

**Réponse attendue** :

```json
{
  "data": {
    "createUserLogin": {
      "userLogin": {
        "id": 1,
        "username": "alice",
        "email": "alice@mail.com"
      }
    }
  }
}
```

**Erreurs possibles** :

* `USERNAME_ALREAD_EXIST` → nom d’utilisateur déjà utilisé.
* `EMAIL_ALREAD_EXIST` → email déjà utilisé.
* `EMAIL_INVALID` → email invalide.
* `EMPY_FIELD_ERROR` → champ manquant.

---

### 2. Envoyer un code de confirmation par email

```graphql
mutation {
  sendConfirmCode(emailTitle: "Titre du mail", userPassword: "motdepasse") {
    isCodeSend
  }
}
```

**Réponse attendue** :

```json
{
  "data": {
    "sendConfirmCode": {
      "isCodeSend": true
    }
  }
}
```

**Erreurs possibles** :

* `INVALID_PASSWORD` → mot de passe incorrect.
* `USER_EMAIL_EMPTY` → utilisateur n’a pas d’email enregistré.

---

### 3. Vérifier le compte utilisateur

```graphql
mutation {
  verifyUserAccount(verificationCode: "123456") {
    accountIsVerified
  }
}
```

**Réponse attendue** :

```json
{
  "data": {
    "verifyUserAccount": {
      "accountIsVerified": true
    }
  }
}
```

**Erreurs possibles** :

* `VERIFICATION_CODE_INVALID` → code invalide.
* `VERIFICATION_CODE_EXPIRED` → code expiré.

---

### 4. Changer le mot de passe

```graphql
mutation {
  changePassword(verificationCode: "123456", newPassword: "nouveauMDP") {
    isPasswordChanged
  }
}
```

**Erreurs possibles** :

* `VERIFICATION_CODE_INVALID` → code invalide.
* `VERIFICATION_CODE_EXPIRED` → code expiré.
* `PASSWORD_IS_TO_SHORT` → mot de passe trop court (<6 caractères).

---

### 5. Réinitialiser le mot de passe d’un élève (enseignant)

```graphql
mutation {
  resetStudentPassword(studentUsername: "eleve1") {
    isPasswordReset
  }
}
```

**Réponse attendue** : `true` si succès.

---

### 6. Supprimer son propre compte

```graphql
mutation {
  deleteUserAccount(verificationCode: "123456") {
    isAccoundDeleted
  }
}
```

**Erreurs possibles** :

* `VERIFICATION_CODE_INVALID` → code invalide.
* `VERIFICATION_CODE_EXPIRED` → code expiré.

---

### 7. Supprimer le compte d’un élève (enseignant)

```graphql
mutation {
  deleteStudentAccount {
    isAccountDeleted
  }
}
```

---

### 8. Supprimer n’importe quel compte (admin)

```graphql
mutation {
  adminDeleteAccount(username: "utilisateur") {
    isAccountDeleted
  }
}
```

**Erreurs possibles** :

* `OPERATION_DENIED-<username>` → utilisateur courant n’est pas admin.
* `USER_NOT_EXIST` → utilisateur inexistant.

---

### 9. Donner les droits admin à un professeur

```graphql
mutation {
  giveAdminAccess(userUsername: "professeur1") {
    isGiveAccessSuccess
  }
}
```

**Erreurs possibles** :

* `OPERATION_DENIED` → utilisateur courant n’est pas admin.
* `USER_NOT_EXIST` → utilisateur inexistant.

---

### 10. Authentification et gestion des tokens

* **Obtenir un token JWT** :

```graphql
mutation {
  tokenAuth(username: "alice", password: "motdepasse") {
    token
    payload
  }
}
```

* **Vérifier un token** :

```graphql
mutation {
  verifyToken(token: "JWT_TOKEN") {
    payload
  }
}
```

* **Rafraîchir un token** :

```graphql
mutation RefreshToken($token: String!) {
  refreshToken(token: $token) {
    token
    payload
    refreshExpiresIn
  }
}
```

**Variables GraphQL** :

```json
{
  "token": "TON_REFRESH_TOKEN"
}
```

**Erreurs possibles** :

* `Signature has expired` → token expiré.
* `Invalid token` → token invalide.

---

## 🔹 Conseils pour l’utilisation

1. Toujours utiliser un token valide pour les mutations nécessitant l’authentification (`@login_required`).
2. Les codes de vérification expirent au bout de 10 minutes.
3. Pour les mutations sensibles (changer mot de passe, suppression de compte), **toujours vérifier le code envoyé par email**.
4. Pour les admins, **vérifier les droits avant de manipuler les comptes d’autres utilisateurs**.

---
