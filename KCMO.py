import json
import requests
import uuid
import pandas as pd
import boto3
    
def lambda_handler(event, context):
    contracts = pd.read_csv('https://data.kcmo.org/api/views/c46m-hv6s/rows.csv')
    contracts['title'] = contracts['Department']+' ('+contracts['Description']+')'
    contracts['suppliers'] = contracts['Vendor']
    contracts['contract_number'] = contracts['Contract Number']
    contracts['contract_amount'] = contracts['Contract Amount']
    contracts['effective'] = contracts['Contract Date']
    cols = [0,1,2,3,4,5,6]
    contracts.drop(contracts.columns[cols],axis=1,inplace=True)
    conts = contracts.to_dict('records')
    for x in conts:
        x.update({
            'id' : (str(uuid.uuid4())),
            'type' : 'add',
            'fields' : {
                'buyer_lead_agency' : 'City of Kansas City, Missouri',
                'states' : 'MO',
                'contract_amount' : x['contract_amount'],
                'contract_number' : x['contract_number'],
                'title' : x['title'],
                'effective' : x['effective'],
                'suppliers' : x['suppliers'],
            }
        })
        del x['contract_amount'], x['contract_number'], x['title'], x['effective'], x['suppliers']
    
    for x in conts:
        filename = x['id']+'.json'
        with open(filename, 'a+', encoding='utf-8') as outfile:
            json.dump(x, outfile)
            body = outfile.read()
            client = boto3.client('s3')
            response = client.put_object( 
            Bucket='coprocure-initial-scrape-repository',
            Body=body,
            Key='kcmo/'+filename
            )
