import os
import re
import random
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration
IMAGE_DIR = os.path.join('static', 'images_animaux')
USERS_FILE = "users.json"
USER_SCORES_DIR = os.path.join('user_scores')

# Créer le répertoire pour les scores des utilisateurs s'il n'existe pas déjà
os.makedirs(USER_SCORES_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clé secrète pour les sessions

# Chargement des utilisateurs depuis un fichier JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Fonction pour charger les scores d'un utilisateur spécifique
def load_user_scores(username):
    user_scores_file = os.path.join(USER_SCORES_DIR, f'{username}_scores.json')
    if os.path.exists(user_scores_file):
        with open(user_scores_file, 'r') as file:
            return json.load(file)
    return {}

# Fonction pour sauvegarder les scores d'un utilisateur spécifique
def save_user_scores(username, scores):
    user_scores_file = os.path.join(USER_SCORES_DIR, f'{username}_scores.json')
    with open(user_scores_file, 'w') as file:
        json.dump(scores, file, indent=4)

# Calcul du score Elo
def calculate_elo(score_a, score_b, result, k=32):
    expected_a = 1 / (1 + 10 ** ((score_b - score_a) / 400))
    new_score_a = score_a + k * (result - expected_a)
    return new_score_a

# Fonction pour valider le mot de passe
def validate_password(password):
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):  # Majuscule
        return False
    if not re.search(r'[a-z]', password):  # Minuscule
        return False
    if not re.search(r'[0-9]', password):  # Chiffre
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Caractère spécial
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    scores = load_user_scores(username)
    images = [img for img in os.listdir(IMAGE_DIR) if img.endswith(('.png', '.jpg', '.jpeg'))]
    image1, image2 = random.sample(images, 2)

    if request.method == 'POST':
        winner = request.form.get('winner')
        loser = request.form.get('loser')

        # Mise à jour des scores
        score_winner = scores.get(winner, 1500)
        score_loser = scores.get(loser, 1500)

        new_score_winner = calculate_elo(score_winner, score_loser, 1)
        new_score_loser = calculate_elo(score_loser, score_winner, 0)

        scores[winner] = new_score_winner
        scores[loser] = new_score_loser

        save_user_scores(username, scores)

        return redirect(url_for('index'))

    return render_template('index.html', image1=image1, image2=image2)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = load_users()

        # Comparer directement le mot de passe en clair
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validation du mot de passe
        if not validate_password(password):
            flash('Le mot de passe doit comporter au moins 6 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.')
            return render_template('register.html')

        users = load_users()

        if username in users:
            flash('Ce nom d’utilisateur est déjà pris. Veuillez en choisir un autre.')
        else:
            # Stocker le mot de passe sans le hacher (pour démonstration seulement)
            users[username] = password

            with open(USERS_FILE, 'w') as file:
                json.dump(users, file, indent=4)

            # Créer un fichier de scores pour cet utilisateur
            user_scores_file = os.path.join(USER_SCORES_DIR, f'{username}_scores.json')
            with open(user_scores_file, 'w') as file:
                json.dump({}, file, indent=4)

            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/ranking')
def ranking():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    scores = load_user_scores(username)
    
    # Trier les images par score décroissant
    sorted_images = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    return render_template('ranking.html', sorted_images=sorted_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

