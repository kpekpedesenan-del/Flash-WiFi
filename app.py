from flask import Flask, request, jsonify, render_template_string
import uuid

app = Flask(__name__)

# --- 1. CONFIGURATION INITIALE (Tes 5 Exemplaires) ---
config = {
    "nom": "Flash WiFi ⚡",
    "bonus": 30,
    "admin_psw": "1234",  # TON CODE SECRET POUR CHANGER LES PRIX
    "offres": [
        {"id": 0, "nom": "Flash Test", "prix": 100, "duree": "2h"},
        {"id": 1, "nom": "Flash Starter", "prix": 200, "duree": "24h"},
        {"id": 2, "nom": "Flash Premium", "prix": 500, "duree": "3 jours"},
        {"id": 3, "nom": "Flash Giga", "prix": 1000, "duree": "7 jours"},
        {"id": 4, "nom": "Flash Business", "prix": 2500, "duree": "1 mois"}
    ]
}

# --- 2. L'INTERFACE UNIQUE (CLIENT + ADMIN CACHÉ) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #0d1117; color: white; text-align: center; padding: 20px; }
        .card { background: #161b22; border-radius: 15px; padding: 15px; margin: 10px 0; border: 1px solid #30363d; }
        .price { color: #FFD700; font-weight: bold; font-size: 1.3em; }
        .btn { background: #FFD700; color: black; border: none; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; }
        .admin-link { margin-top: 50px; font-size: 0.7em; color: #30363d; text-decoration: none; }
        input { width: 90%; padding: 10px; margin: 5px 0; border-radius: 5px; border: none; }
    </style>
</head>
<body>
    <h1>{{ config.nom }}</h1>
    <p>🎁 Cadeau : <b>{{ config.bonus }} min</b> à l'inscription</p>

    {% for o in config.offres %}
    <div class="card">
        <b>{{ o.nom }}</b><br>
        <span class="price">{{ o.prix }} FCFA</span> / {{ o.duree }}<br><br>
        <button class="btn">Acheter via MTN / Moov</button>
    </div>
    {% endfor %}

    <a href="/admin-login" class="admin-link">Espace Professeur</a>
</body>
</html>
"""

# --- 3. LES ROUTES ---

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, config=config)

@app.route('/admin-login')
def admin_page():
    return """
    <body style="background:#0d1117; color:white; text-align:center; padding:50px;">
        <h2>🔐 Connexion Admin</h2>
        <form action="/update-config" method="POST">
            <input type="password" name="psw" placeholder="Code Secret" style="padding:10px;"><br><br>
            <p>Changer le prix du Forfait 1 (100F) :</p>
            <input type="number" name="nouveau_prix" placeholder="Nouveau prix en FCFA"><br><br>
            <button type="submit" style="background:#FFD700; padding:10px;">Enregistrer les changements</button>
        </form>
    </body>
    """

@app.route('/update-config', methods=['POST'])
def update():
    password = request.form.get('psw')
    nouveau_prix = request.form.get('nouveau_prix')
    
    if password == config['admin_psw']:
        if nouveau_prix:
            config['offres'][0]['prix'] = int(nouveau_prix) # Change le 1er forfait
        return "<h3>✅ Changement réussi ! <a href='/'>Retour à l'appli</a></h3>"
    else:
        return "<h3>❌ Code incorrect !</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
