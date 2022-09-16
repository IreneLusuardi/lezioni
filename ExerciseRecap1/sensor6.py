#
from secret import secret
from requests import get, post
import time
import json
#è UGUALE AL SENSORE 4, è la function che deve cambiare e inviare i dati a big query e non su firestore
#non do al sensore 6 un file credentials.json che consente di salvare i dati su db, ma solo l'url di una function
function_url = 'https://europe-west1-testlez11-362216.cloudfunctions.net/save_data_bq'
with open('CleanData_PM10.csv') as f:
    for r in f:
        r = r.strip()
        t,pm10 = r.split(',')
        pm10 = float(pm10)
        r = post(function_url, data = {'data': json.dumps({'sensor':'sensor6','time': t, 'pm10': pm10, 'secret':secret})})
        print('sending',t,pm10,' -----> ',r.status_code)
        time.sleep(10)
