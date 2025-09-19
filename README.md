````markdown
# 📘 Documentation API – Gestion des Comptes Utilisateurs

Cette API GraphQL permet la gestion des utilisateurs (création, vérification, mots de passe, suppression, etc.).  
Toutes les requêtes s’effectuent via des **mutations GraphQL**.  
L’authentification se fait avec **JWT** (token d’accès obtenu via `tokenAuth`).  

---

## 🔑 Authentification

### Mutation `tokenAuth`

Permet de récupérer un **JWT token** pour s’authentifier.

#### Exemple de requête

```graphql
mutation {
  tokenAuth(username: "john", password: "mypassword") {
    token
  }
}
````

#### Résultat attendu

```json
{
  "data": {
    "tokenAuth": {
      "token": "eyJ0eXAiOiJKV1QiLCJh..."
    }
  }
}
```

#### Erreurs possibles

* `INVALID_CREDENTIALS` → Mauvais identifiants
* `USER_NOT_FOUND` → Utilisateur inexistant

👉 L’utilisateur doit vérifier son identifiant et mot de passe.

---

## 👤 Créer un utilisateur

### Mutation `createUserLogin`

Crée un nouveau compte utilisateur.

#### Arguments

* `username` *(String, requis)*
* `password` *(String, requis)*
* `email` *(String, optionnel)*

#### Exemple

```graphql
mutation {
  createUserLogin(username: "john", password: "123456", email: "john@example.com") {
    userLogin {
      id
      username
      email
    }
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "createUserLogin": {
      "userLogin": {
        "id": "1",
        "username": "john",
        "email": "john@example.com"
      }
    }
  }
}
```

#### Erreurs possibles

* `EMAIL_ALREAD_EXIST` → l’email existe déjà
* `EMAIL_INVALID` → email non valide
* `USERNAME_ALREAD_EXIST` → username déjà pris
* `EMPY_FIELD_ERROR` → champs manquants

---

## 📧 Envoyer un code de confirmation

### Mutation `sendConfirmCode`

Envoie un code de confirmation à l’utilisateur par email.
⚠️ **Requiert authentification avec token JWT.**

#### Arguments

* `emailTitle` *(String, requis)* → Titre du mail
* `userPassword` *(String, requis)* → Mot de passe de l’utilisateur

#### Exemple

```graphql
mutation {
  sendConfirmCode(emailTitle: "Vérification Compte", userPassword: "123456") {
    isCodeSend
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "sendConfirmCode": {
      "isCodeSend": true
    }
  }
}
```

#### Erreurs possibles

* `INVALID_PASSWORD` → mot de passe incorrect
* `USER_EMAIL_EMPTY` → aucun email associé à l’utilisateur

👉 L’utilisateur doit d’abord avoir un email valide.

---

## ✅ Vérifier un compte utilisateur

### Mutation `verifyUserAccount`

Valide le compte via un code reçu par email.
⚠️ Requiert authentification.

#### Arguments

* `verificationCode` *(String, requis)*

#### Exemple

```graphql
mutation {
  verifyUserAccount(verificationCode: "123456") {
    accountIsVerified
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "verifyUserAccount": {
      "accountIsVerified": true
    }
  }
}
```

#### Erreurs possibles

* `VERIFICATION_CODE_INVALID`
* `VERIFICATION_CODE_EXPIRED`

---

## 🔐 Changer le mot de passe

### Mutation `changePassword`

Permet de modifier le mot de passe via un code reçu par mail.
⚠️ Requiert authentification.

#### Arguments

* `verificationCode` *(String, requis)*
* `newPassword` *(String, requis, min 6 caractères)*

#### Exemple

```graphql
mutation {
  changePassword(verificationCode: "123456", newPassword: "newpass123") {
    isPasswordChanged
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "changePassword": {
      "isPasswordChanged": true
    }
  }
}
```

#### Erreurs possibles

* `VERIFICATION_CODE_INVALID`
* `VERIFICATION_CODE_EXPIRED`
* `PASSWORD_IS_TO_SHORT`

---

## 🗑️ Supprimer son compte

### Mutation `deleteUserAccount`

Supprime définitivement le compte de l’utilisateur.
⚠️ Requiert authentification + code de vérification.

#### Arguments

* `verificationCode` *(String, requis)*

#### Exemple

```graphql
mutation {
  deleteUserAccount(verificationCode: "123456") {
    isAccoundDeleted
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "deleteUserAccount": {
      "isAccoundDeleted": true
    }
  }
}
```

#### Erreurs possibles

* `VERIFICATION_CODE_INVALID`
* `VERIFICATION_CODE_EXPIRED`

---

## 🛠️ Supprimer un compte en tant qu’administrateur

### Mutation `adminDeleteAccount`

Permet à un administrateur de supprimer un compte utilisateur par son username.
⚠️ Requiert authentification en tant que **superuser**.

#### Arguments

* `username` *(String, requis)*

#### Exemple

```graphql
mutation {
  adminDeleteAccount(username: "john") {
    isAccountDeleted
  }
}
```

#### Résultat attendu

```json
{
  "data": {
    "adminDeleteAccount": {
      "isAccountDeleted": true
    }
  }
}
```

#### Erreurs possibles

* `OPERATION_DENIED-<username>` → pas admin
* `USER_NOT_EXIST` → utilisateur inexistant

---

## 🔄 Gestion des Tokens

### Mutation `verifyToken`

Vérifie si un token est encore valide.

```graphql
mutation {
  verifyToken(token: "xxx") {
    payload
  }
}
```

Exemple d’erreur si token expiré :

```json
{
  "errors": [
    {
      "message": "Signature has expired"
    }
  ],
  "data": {
    "verifyToken": null
  }
}
```

👉 Dans ce cas, l’utilisateur doit demander un **refresh token**.

---

# 📌 Résumé des erreurs globales

| Erreur                        | Cause                          | Solution utilisateur              |
| ----------------------------- | ------------------------------ | --------------------------------- |
| `INVALID_PASSWORD`            | Mot de passe erroné            | Vérifier les identifiants         |
| `USER_EMAIL_EMPTY`            | Aucun email associé            | Ajouter un email valide           |
| `EMAIL_ALREAD_EXIST`          | Email déjà pris                | Utiliser un autre email           |
| `USERNAME_ALREAD_EXIST`       | Username déjà pris             | Choisir un autre identifiant      |
| `EMAIL_INVALID`               | Email mal formaté              | Fournir une adresse valide        |
| `EMPY_FIELD_ERROR`            | Champs manquant                | Vérifier la requête               |
| `VERIFICATION_CODE_INVALID`   | Code inexistant                | Vérifier le code reçu             |
| `VERIFICATION_CODE_EXPIRED`   | Code expiré (10 min)           | Demander un nouveau code          |
| `PASSWORD_IS_TO_SHORT`        | Mot de passe trop court (<6)   | Fournir un mot de passe plus long |
| `OPERATION_DENIED-<username>` | Tentative admin sans privilège | Se connecter avec un compte admin |
| `USER_NOT_EXIST`              | Utilisateur inexistant         | Vérifier l’username               |

```
```
