import boto3
import json
import logging
import sys
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Customer_Profile')
ses = boto3.client('ses')
apigateway = boto3.client('apigateway')

#SES declarations
source_email = "---"
charset = 'utf-8'

def fetch_customer_profile(customer_id):
    try:
        response = table.get_item(
            Key = {
                'customer_id': customer_id
            }
        )
        
        sms_consent = response['Item']['sms_consent']
        logger.info(f"dyanomodb response {response}")
        return sms_consent
    
    except Exception as e:
        logger.error(f"Could not fecth customer profile data: {e}")
        sys.exit(1)


def send_email(dest_email, customer_id, customer_name, invoice_number, invoice_date):
    try:
        response = ses.send_email(
            Source = source_email,
            Destination = {
                'ToAddresses': [
                    dest_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Bill Notification',
                    'Charset': charset
                },
                'Body': {
                    'Text': {
                        'Data': f"Your current month bill is ready to view. Please login to your account to review your bill.\n\
                        Customer ID : {customer_id}\n\
                        Customer Name : {customer_name}\n\
                        Invoice Number: {invoice_number}\n\
                        Invoice Date: {invoice_date}",
                        'Charset': charset
                    }
                }
            }
        )
    
        logger.info(f"ses response {response}")
    
    except Exception as e:
        logger.error(f"Could not send email: {e}")
        return None
        

def send_sms(phone_number):
    api_url = 'https://cz8qgumdwk.execute-api.us-east-1.amazonaws.com/v1/service/sms'

    payload = {
        'phone_number': phone_number,
        'sms_content': 'Your current month bill is ready to view. Please login to your account to review your bill.'
    }

    json_payload = json.dumps(payload)

    http = urllib3.PoolManager()

    response = http.request('POST', api_url, body=json_payload, headers={'Content-Type': 'application/json'})
    
    print(response.status)
    print(response.data)

    
def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_name = event['Records'][0]['s3']['object']['key']
    
    response = s3.get_object(Bucket = bucket_name, Key = object_name)
    data = response['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    
    customer_id, customer_name, invoice_number, invoice_date, phone_number, email_id, bill_amount = json_data.values()
    
    sms_consent = fetch_customer_profile(customer_id)
    
    if sms_consent == 'Yes':
        send_sms(phone_number)
    else:
        send_email(email_id,customer_id, customer_name, invoice_number, invoice_date )
    



    

    
