import csv
import boto3
import json
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
output_key = 'individual-json/'


def lambda_handler(event,context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_name = event['Records'][0]['s3']['object']['key']
   
    response = s3.get_object(Bucket = bucket_name, Key = object_name)
    data = response['Body'].read().decode('utf-8').splitlines()
    milliseconds = round(time.time() * 1000)
    
    try:
    
        for row in csv.DictReader(data,delimiter='|'):
            
            if row != []:
                customer_id, customer_name, invoice_number, invoice_date, phone_number, email_id, bill_amount = row.values()
                json_object = row
                s3.put_object(
                     Body=json.dumps(json_object),
                     Bucket=bucket_name,
                     Key=f"{output_key}{customer_id}-{milliseconds}.json"
                )
        logger.info(f"Successfully created individual files")
        
    except Exception as e:
        logger.error(f"Could not read input file: {e}")
        