# data-pipeline-scraper
This is used to store the lambda code to scrape contracts and copy them to the S3 bucket 'coprocure-initial-scrape-repository'

Each of these scrapers is similar to their code for a local deployment, but must include the following additions:

    'import boto3' 
for working with S3 and AWS from within Python, as well as the following code below at the end:

    for x in records:
   
        filename = x['id']+'.json'
    
        ## records have to be encoded in order to write to S3 from python

        with open(filename, 'a+', encoding='utf-8') as outfile:
            json.dump(x, outfile)

            body = outfile.read()

            client = boto3.client('s3')

            response = client.put_object( 

            ## no security for this particular bucket - mimicking the setup of other S3 buckets; advise if changes should be made

            Bucket='coprocure-initial-scrape-repository',

            Body=body,

            ## key named for subfolder according to source

            Key='esc19/'+filename)

This will enable you to scrape directly from your Python environment and write to the S3 bucket.

In order to deploy these scrapers to AWS, you will need to follow these steps:

1. Write your Python script. Make sure all packages are imported at the top of the script, and that the functionality is defined as a function 'lambda_handler(event, context):'
2. Create a directory on your local machine containing the Python script.
3. Install all necessary packages and dependencies to that directory using the following format:
    'pip install {pkg} -t ./'
4. Zip all the contents of this folder within the directory.
5. Create a new Lambda on AWS. Select US-East-1 (N. Virginia).
6. Select Python 3.7 as your runtime, and arc-role as the permission role.
7. When editing the code, select 'Upload from .zip file' and use the zipped folder from above
8. Connect it to an API or S3 trigger as necessary.

Some heavier scrapers may time out. In order to avoid this, consider running them locally to write to S3. To run this locally, run the code located in the scraping-v2-python repository in any standard Python environment.

