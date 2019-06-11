import json
import boto3
import requests

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('coprocure-initial-scrape-repository')
    new = {}
    for obj in bucket.objects.all():
        k = obj.key.split('/')[:1]
        cn = []
        tt = []
        ids = []
        try:
            body = obj.get()['Body'].read().decode('utf-8').replace('\0', '')
            jbody = json.loads(body)
            cn.append(jbody['fields']['contract_number'])
            tt.append(jbody['fields']['title'])
            ids.append(jbody['fields']['id'])
            for (x,y, z) in zip(cn, tt, ids):
                url1 = 'https://9mmq83tcuh.execute-api.us-west-2.amazonaws.com/production/?source_key='+k+'&contract_number='+x
                url2 = 'https://9mmq83tcuh.execute-api.us-west-2.amazonaws.com/production/?source_key='+k+'&title='+y
                r1 = requests.get(url1).json()
                r2 = requests.get(url2).json()
                if r1 == r2:
                    pass
                else:
                    filename = z+'.json'
                    with open(filename, 'a+', encoding='utf-8') as outfile:
                        json.dump(jbody, outfile)
                        body = outfile.read()
                        client = boto3.client('s3')
                        response = client.put_object( 
                        Bucket='data-pipeline-pre-s3',
                        Body=body,
                        Key=k+filename
                        )
        except:
            pass
