# Facemash des Animaux

Ce projet est un jeu de classement d'images d'animaux basé sur les préférences des utilisateurs. Les utilisateurs peuvent se connecter, choisir entre deux animaux et leur score sera mis à jour selon un système de classement Elo.

## Structure du Projet

```
project/
│
├── static/                       
│   └── images_animaux/                
│       ├── image_1.png
│       └── image_2.png
│
├── templates/                    
│   ├── index.html
│   ├── login.html
│   ├── ranking.html
│   └── register.html
│ 
├── user_scores/                    
│   ├── user_name_1.json
│   └── user_name_2.json
│
├── app.py
|
├── users.json
|
└── README.md
```

## Configuration

### Prérequis

- Python 3.8+
- Flask
- Werkzeug
- ngrok (pour le déploiement sur internet)

### Installation

Clonez le dépôt et installez les dépendances :

```bash
git clone https://yourrepository.com/facemash_animaux.git
cd facemash_animaux
pip install flask werkzeug
```

### Configuration de l'Application

Avant de lancer l'application, assurez-vous de définir une clé secrète pour les sessions dans `app.py` :

```python
app.secret_key = 'votre_clé_secrète'
```

### Lancement de l'Application

Pour exécuter l'application localement :

```bash
python app.py
```

L'application sera accessible à l'adresse `http://localhost:5000`.

## Utilisation de ngrok pour l'accès Internet

Pour rendre votre application accessible sur Internet, utilisez ngrok. Si ngrok n'est pas installé, vous pouvez le télécharger et l'installer depuis [ngrok.com](https://ngrok.com/).

Exécutez ngrok avec la commande suivante :

```bash
ngrok http --domain=funny-devoted-dinosaur.ngrok-free.app 5000
```

Cela créera un tunnel sécurisé vers `localhost:5000` et rendra votre application accessible à l'adresse fournie par ngrok, par exemple `http://funny-devoted-dinosaur.ngrok-free.app`.