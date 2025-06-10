# 🛡️ PasswordVault

**PasswordVault** est un gestionnaire de mots de passe local et sécurisé, développé en Python avec une interface graphique moderne grâce à Tkinter.  
Il permet à chaque utilisateur de créer un compte personnel et de gérer facilement ses identifiants pour tous ses services (sites web, applications, etc.).

---

## ✨ Fonctionnalités principales

- **Création de compte et connexion sécurisée**
- **Ajout, affichage, modification et suppression de mots de passe**
- **Recherche rapide d’un mot de passe par nom de site**
- **Génération automatique de mots de passe robustes**
- **Stockage local chiffré des données (aucune donnée envoyée sur Internet)**
- **Interface graphique simple et intuitive**
- **Architecture modulaire (authentification, gestion, chiffrement séparés)**

---

## 🔒 Sécurité

- Les mots de passe sont chiffrés localement avec la bibliothèque `cryptography` (Fernet).
- Chaque utilisateur possède son propre coffre-fort chiffré.
- Le mot de passe maître n’est jamais stocké en clair.

---

## 🖼️ Aperçu

_Ajoutez ici une capture d’écran de l’application si vous le souhaitez !_  
`doc/screenshot.png`

---

## 🚀 Installation & Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/MrsHaro/password-vault.git
cd password-vault
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l’application

```bash
python main.py
```

---

## 🧰 Technologies utilisées

- Python 3
- Tkinter (interface graphique)
- cryptography (chiffrement Fernet)
- JSON (stockage local des données)

---

## 👤 Auteur

Arthur TCHANDA

Contact: arthurtchanda@gmail.com

---

## 📄 Licence

Ce projet est open-source sous licence MIT.

---

## 💡 Remarques

- **Aucune donnée n’est envoyée sur Internet.** Tout reste sur votre ordinateur.