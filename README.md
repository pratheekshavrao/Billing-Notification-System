
# Billing Notification System

The billing notification system utilizes AWS services to streamline communication between a company and its customers. Third-party vendors upload invoice files securely via SFTP using AWS Transfer service, which are then stored in a S3 bucket. These invoice files are processed and split into individual files for each customer, stored in an S3 bucket. Lambda functions fetch customer information from a database to determine SMS consent opted by the customer. For customers who have opted for SMS consent, API Gateway integrates with a third-party SMS service to send billing notifications. Alternatively, for customers without SMS consent, notifications are sent through email via Amazon SES service. This system ensures efficient, personalized communication while leveraging AWS scalability and reliability.


## Pre – requisites:

Create an S3 bucket named billing-notification-system with Input prefix. Also create an event notification trigger when files get uploaded into this path which triggers an Input File Split lambda function.

## Steps for execution:

1.	Sign into AWS console. Navigate to AWS Transfer service and create an SFTP server with the appropriate settings.
   
    ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP-Server_1.jpg)

    ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_Server2.jpg)
  	
   
2.	Once the server is setup, then add users to it by giving them appropriate permissions to access the S3 bucket into which files are to be uploaded.

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_User_1.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_User_2.jpg)
   
   
3.	By using WinSCP tool, input the server access credentials and securely upload the invoice file which gets uploaded into S3 bucket into Input folder.

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_Access_1.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_Access_2.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_Login_Screen.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_File_Upload_1.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/SFTP_File_Upload_2.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/S3_InputFile_Uploaded.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Input_file.jpg)
   
   
4.	The file uploaded into the bucket will trigger Input File Split lambda function.

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Input_File_Split_Trigger.jpg)
   
   
5.	The Input File Split lambda function will split the records read from invoice file into individual json files for each customer. These files are stored in /individual-json prefix in the same S3 bucket.

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Input_File_Split_Lambda.jpg)
   
   
6.	These individual files created will inturn trigger another lambda function called Bill Notification Process.

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Bill_Notification_Process_Trigger.jpg)

   
7.	The Bill Notification Process lambda will read each individual file and fetch customer data from Customer Profile table to determine the SMS consent pre-selected by the customer. ( DynaomoDB table has been pre-created and populated with Customer Profile data with customer_id as partition key).

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Bill_Notification_Process_Lambda.jpg)

   ![alt text](https://github.com/pratheekshavrao/Billing-Notification-System/blob/main/images/Customer_Profile_table.jpg)

   
8.	For local testing of Lambda functions, download the functions to Cloud9 environment, create event.json and template .yaml files. Use below code from terminal to test the functions.
    
9.	Once local testing is successful, upload the Lambda functions into AWS console. For Input File Split function add permissions to access S3 to the execution role. Similarly for Bill Notification Process function, add permissions to access S3, DynamoDB, SES and API Gateway.
    
10.	If SMS consent is Yes, then a SMS is sent to the customer using third party application via API Gateway. For this configure a MOCK integration on API Gateway with POST method.
15.	 If SMS consent is No, then an email is sent to the customer using SES service. For testing purposes, verify the Identities of the destination email ids in the SES console.

## Result and Observations:

•	For those customers with SMS consent as Yes a mock SMS is sent via API Gateway.

•	For those customers with SMS consent as No an email is sent via SES service.
