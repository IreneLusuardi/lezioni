
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from google.cloud import firestore
from secret import secret, secret_key, usersdb
import json
from base64 import b64decode

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {} #se l'utente ha dei parametri specifici si possono inserire qui

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app) #login manager che si occupa del login
login.login_view = '/static/login.html' #imposta pag html in cui ci sarà form html associata al manager del login.
#automaticamente flask capisce, quando sto cercando id accedere a una pag che richiede il login, flask mi rimanda in auto alla pagina del login


@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None


@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sensors/<sensor>',methods=['GET'])
def read_all(sensor):
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    data = [] #per leggere la lista di liste
    for doc in db.collection(sensor).stream():
        x = doc.to_dict() #tengo un dizionario a partire dal documento
        data.append([x['time'].split(' ')[0],float(x['value'])]) #appendo una lista dove al primo elemento ho time e al secondo il valore, converto in float
    return json.dumps(data)
    # [['2020-01-01',  40.5],....]


def soglia(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    # db = firestore.Client()
    data = []
    for doc in db.collection('sensor1').stream(): #scorre i dati
        x = doc.to_dict() #li converte in dizionario
        if float(x['value']) > s: #se il valore è maggiore della soglia
            data.append(x['time'].split(' ')[0]) #aggiungi la data in cui si è bverificato il valore superiore alla soglia
    return json.dumps(data)


@app.route('/graph/<sensor>',methods=['GET']) #permette di visualizzare tutti i dati
@login_required
def graph(sensor):
    data = json.loads(read_all(sensor)) #read all ritorna una stringa json con i dati, loads trasforma la stringa json in variabili e rimette data con variabile python che rappresenta la stringa json
    data.insert(0,['Time', 'Pm10'])
    return render_template('graph.html',data=data,soglia=json.loads(soglia(80)))


@app.route('/sensors/sensor1',methods=['POST']) #salva nella collezione sensor1 i dati e il timestamp
def save_data():
    s = request.values['secret']
    if s == secret:
        time = request.values['time'] #qui le leggo come stringhe
        pm10 = request.values['pm10']
        db = firestore.Client.from_service_account_json('credentials.json')
        #db = firestore.Client()
        db.collection('sensor1').document(time).set({'time': time, 'value': pm10})
        return 'ok', 200
    else:
        return '', 401


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username), remember=True) #lo mantiene loggato e l'utente può visitare le pagine che hanno login required, mantiene loggato anche quando chiudo le finestre(31 GG)
        next_page = request.args.get('next')
        if not next_page:
            next_page = '/'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/pubsub/receive',methods=['POST'])
def pubsub_push():
    dict = json.loads(request.data.decode('utf-8'))
    print(dict)
    msg = json.loads(dict['message']['attributes']['payload'])
    print(msg)
    # {'sensor': client_id, 'time': t, 'pm10': pm10})
    db = firestore.Client.from_service_account_json('credentials.json') #vedi in simple consumer come si aggancia al db
    db.collection(msg['sensor']).document(msg['time']).set({'time': msg['time'], 'value': msg['pm10']})
    return 'OK',200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

