# Projet de Publication d'Annonces

Ce projet est une plateforme web permettant aux utilisateurs de publier et gérer des annonces. Il est développé avec Django pour le backend et Angular pour le frontend.

## Prérequis

Avant d'exécuter ce projet, assurez-vous d'avoir installé :
- [Python](https://www.python.org/downloads/) (>= 3.8)
- [Node.js](https://nodejs.org/) et npm
- [PostgreSQL](https://www.postgresql.org/) (ou une autre base de données compatible)

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Abeidak/Annonce.git
cd Annonce
```

### 2. Création de l'environnement virtuel

```bash
python -m venv env
source venv/bin/activate  # Sur macOS/Linux
venv\Scripts\activate  # Sur Windows
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données

Modifiez le fichier `.env` en ajoutant vos informations de base de données :

```
DATABASE_NAME=nom_de_votre_base
DATABASE_USER=utilisateur
DATABASE_PASSWORD=mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Appliquez ensuite les migrations :

```bash
python manage.py migrate
```

### 5. Création d'un super-utilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```
Accédez au site via `http://127.0.0.1:8000/`

<!-- ## Développement Frontend
Si vous utilisez Angular pour le frontend, naviguez vers le dossier frontend et démarrez le projet :

```bash
cd frontend
npm install
ng serve
```

## Déploiement
Pour déployer le projet, vous pouvez utiliser Docker, Heroku ou un autre service cloud. Assurez-vous d'ajouter les configurations nécessaires pour le fichier `.env` et les paramètres de production.

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence
Ce projet est sous licence MIT. -->