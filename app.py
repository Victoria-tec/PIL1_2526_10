from flask import Flask        # on importe Flask

app = Flask(__name__)          # on crée l'application

@app.route('/')                # quand quelqu'un va sur la page d'accueil
def accueil():                 # cette fonction s'exécute
    return 'Bienvenue !'       # et renvoie ce texte

if __name__ == '__main__':     # si on lance ce fichier directement
    app.run(debug=True)        # on démarre le serveur