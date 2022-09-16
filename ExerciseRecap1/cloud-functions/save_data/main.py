def save_data(request): #function che salva i dati, usata con sensor4
    from google.cloud import firestore
    import json
    if request.method == 'OPTIONS': #questo meccanismo serve per sensor5.html che invia i dati con javascript
        #quando il browser fa una richiesta http a questa fuction, il browser prima di inviare la post invia un'altra richiesta allo stesso url con metodo options
        #il server risponde dicendo quello che posso fare in risposta a questa pagina:
        print('------ options')
        # Allows GET and POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*', #da qualunque parte della reta
            'Access-Control-Allow-Methods': 'GET,POST', #puoi fare get o post
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

#rigeh vere e proprio di quello che fa la funzione
    # qua si potrebbe mettere un if di sicurezza sul secret
    msg = json.loads(request.values['data'])
    #request_json = request.data.decode('utf-8')
    print('>>>>>>>>>>>>>>>>>>>>>>>')
    print(msg)
    db = firestore.Client()
    db.collection(msg['sensor']).document(msg['time']).set({'time': msg['time'], 'value': msg['pm10']})

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return ('ok', 200, headers)
