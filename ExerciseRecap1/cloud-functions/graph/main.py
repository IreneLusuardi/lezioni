def graph(request): #function graph, usata con
    from flask import render_template
    from google.cloud import firestore
    import json
#definisco una funzione entro a una funzione
    def read_all(sensor):
        db = firestore.Client() #mi collego a firestore
        data = []
        for doc in db.collection(sensor).stream(): #leggo i dati
            x = doc.to_dict() #non c'è parte su cors!!
            data.append([x['time'].split(' ')[0], float(x['value'])])
        return json.dumps(data)

#parte copiata dal main di ExRecap11 funzione graph
    sensor = request.values['sensor']
    data = json.loads(read_all(sensor)) #sensor prima veniva da un parametro che passavo come url, ora uso questo stratagemma
    data.insert(0, ['Time', 'Pm10'])
    return render_template('graph.html', data=data)
