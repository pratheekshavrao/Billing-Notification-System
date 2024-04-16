
# Billing Notification System

The billing notification system utilizes AWS services to streamline communication between a company and its customers. Third-party vendors upload invoice files securely via SFTP using AWS Transfer service, which are then stored in a S3 bucket. These invoice files are processed and split into individual files for each customer, stored in an S3 bucket. Lambda functions fetch customer information from a database to determine SMS consent opted by the customer. For customers who have opted for SMS consent, API Gateway integrates with a third-party SMS service to send billing notifications. Alternatively, for customers without SMS consent, notifications are sent through email via Amazon SES service. This system ensures efficient, personalized communication while leveraging AWS scalability and reliability.


## Pre – requisites:

Create an S3 bucket named billing-notification-system with Input prefix. Also create an event notification trigger when files get uploaded into this path which triggers an Input File Split lambda function.
