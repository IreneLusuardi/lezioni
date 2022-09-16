def save_data_bq(request):
    #copiata da save_data main ma cambia i requirements
    from secret import secret
    from google.cloud import bigquery
    import json
    if request.method == 'OPTIONS':
        print('------ options')
        # Allows GET and POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)


    msg = json.loads(request.values['data'])
    print('>>>>>>>>>>>>>>>>>>>>>>>')
    print(msg)
#questa parte copiata da test_local di lez 16
    if msg['secret'] == secret: #solo i sensori che conoscono la key possono accedere ai dati nel datastore
        project_id = 'testlez11-362216'
        dataset_id = 'sensors'
        table_id = 'sensors'
        client = bigquery.Client()
        table_full_id = f'{project_id}.{dataset_id}.{table_id}'
#eliminate le righe che servono per memorizzare il dato in firestore
#copio dal primo insert
        rows_to_insert = [{'sensor':msg['sensor'],'time': msg['time'], 'value': msg['pm10']}]
        errors = client.insert_rows_json(table_full_id, rows_to_insert)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        return ('ok', 200, headers)
    else:
        return ('not authorized',401,{'Access-Control-Allow-Origin': '*'})
