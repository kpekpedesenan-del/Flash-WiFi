from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- CONFIGURATION (MISE À JOUR) ---
PUBLIC_KEY = "pk_live_oI1Z_UNXCvhmVAhfGdbwLFN" 
# MODIFIE TON CODE ADMIN ICI (ex: "7788")
SECRET_ADMIN_CODE = "1234" 

# Base de données des forfaits
forfaits = [
    {"id": 1, "nom": "Flash Test", "prix": 100, "duree": "2h"},
    {"id": 2, "nom": "Flash Starter", "prix": 200, "duree": "24h"},
    {"id": 3, "nom": "Flash Premium", "prix": 500, "duree": "3 jours"},
    {"id": 4, "nom": "Flash Giga", "prix": 1000, "duree": "7 jours"},
    {"id": 5, "nom": "Flash Business", "prix": 2500, "duree": "1 mois"}
]

# Simulation de l'historique que tu voulais voir
# Dans une version future, on connectera une vraie base de données
historique_ventes = [
    {"date": "03/04 09:45", "client": "Utilisateur_88", "forfait": "Flash Starter", "montant": 200, "status": "Payé"},
    {"date": "03/04 10:12", "client": "Utilisateur_12", "forfait": "Flash Giga", "montant": 1000, "status": "Payé"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flash WiFi ⚡</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.fedapay.com/checkout.js?v=1.1.7"></script>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 15px; padding: 15px; margin: 10px auto; max-width: 400px; }
        .btn { background: #facc15; color: black; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 1em; }
        .admin-link { color: #475569; font-size: 0.8em; text-decoration: none; margin-top: 50px; display: block; }
    </style>
</head>
<body>
    <h1>Flash WiFi ⚡</h1>
    <p>Connexion ultra-rapide au Bénin</p>

    {% for f in forfaits %}
    <div class="card">
        <h3>{{ f.nom }}</h3>
        <p style="color:#facc15; font-size: 1.3em; font-weight: bold;">{{ f.prix }} FCFA / {{ f.duree }}</p>
        <button class="btn" id="pay-btn-{{ f.id }}">Acheter via MTN / Moov</button>
        <script>
            document.getElementById('pay-btn-{{ f.id }}').addEventListener('click', function() {
                FedaPay.init('#pay-btn-{{ f.id }}', {
                    public_key: '{{ public_key }}',
                    transaction: {
                        amount: {{ f.prix }},
                        description: 'Achat forfait {{ f.nom }}'
                    }
                });
            });
        </script>
    </div>
    {% endfor %}

    <a href="/admin" class="admin-link">Espace Administration 🔐</a>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard WiFi Admin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
        .stat-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .stat-box { background: #1e293b; padding: 15px; border-radius: 10px; flex: 1; border-top: 4px solid #facc15; }
        table { width: 100%; border-collapse: collapse; background: #1e293b; margin-top: 10px; }
        th, td { padding: 12px; border: 1px solid #334155; text-align: left; font-size: 0.85em; }
        th { background: #334155; color: #facc15; }
        .status { color: #4ade80; font-weight: bold; }
        .back-btn { display: inline-block; margin-top: 20px; color: #facc15; text-decoration: none; }
    </style>
</head>
<body>
    <h2>🔐 Suivi des Ventes WiFi</h2>
    
    <div class="stat-container">
        <div class="stat-box">
            <small>Total Encaissé</small>
            <div style="font-size: 1.5em; font-weight: bold;">1 200 F</div>
        </div>
        <div class="stat-box">
            <small>Ventes du jour</small>
            <div style="font-size: 1.5em; font-weight: bold;">2</div>
        </div>
    </div>

    <h3>Historique des paiements (Public)</h3>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Forfait</th>
                <th>Montant</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            {% for v in historique %}
            <tr>
                <td>{{ v.date }}</td>
                <td>{{ v.forfait }}</td>
                <td>{{ v.montant }} F</td>
                <td class="status">{{ v.status }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <a href="/" class="back-btn">← Retour à l'accueil</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, forfaits=forfaits, public_key=PUBLIC_KEY)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == SECRET_ADMIN_CODE:
            return render_template_string(ADMIN_TEMPLATE, historique=historique_ventes)
        return "Code Incorrect ! <a href='/admin'>Réessayer</a>"
    
    return '''
        <body style="background:#0f172a; color:white; text-align:center; padding-top:100px; font-family:sans-serif;">
            <form method="post">
                <div style="background:#1e293b; display:inline-block; padding:30px; border-radius:15px; border: 1px solid #334155;">
                    <h3>Accès Propriétaire</h3>
                    <input type="password" name="code" placeholder="Code Secret" style="padding:12px; border-radius:5px; border:none; width:200px;"><br><br>
                    <input type="submit" value="Vérifier les ventes" style="padding:12px 25px; background:#facc15; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">
                </div>
            </form>
        </body>
    '''

if __name__ == '__main__':
    app.run(debug=True)

