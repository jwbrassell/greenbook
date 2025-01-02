"""
Boto3 AWS Integration Example
Shows how to interact with AWS services compared to PHP's file operations
"""

from flask import Flask, request, jsonify, send_file
import boto3
from botocore.exceptions import ClientError
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import json

app = Flask(__name__)

"""
PHP File Operations (Limited to Server):
```php
// File Upload
if ($_FILES['file']) {
    move_uploaded_file(
        $_FILES['file']['tmp_name'],
        'uploads/' . $_FILES['file']['name']
    );
}

// File Read
$content = file_get_contents('data/file.txt');

// File List
$files = scandir('uploads/');

// File Delete
unlink('uploads/file.txt');
```
"""

# S3 Operations
def get_s3_client():
    """
    Get S3 client with credentials
    Better than PHP's direct file system access
    """
    return boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload file to S3
    
    Benefits over PHP:
    1. Scalable storage
    2. Automatic replication
    3. Access control
    4. CDN integration
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    try:
        filename = secure_filename(file.filename)
        s3_client = get_s3_client()
        
        # Upload with metadata
        s3_client.upload_fileobj(
            file,
            os.getenv('AWS_BUCKET_NAME'),
            f'uploads/{filename}',
            ExtraArgs={
                'ContentType': file.content_type,
                'Metadata': {
                    'original_filename': filename,
                    'upload_time': datetime.now().isoformat()
                }
            }
        )
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename
        })
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """
    Download file from S3
    
    Benefits over PHP:
    1. No local storage needed
    2. Bandwidth optimization
    3. Access control
    """
    try:
        s3_client = get_s3_client()
        file_obj = BytesIO()
        
        s3_client.download_fileobj(
            os.getenv('AWS_BUCKET_NAME'),
            f'uploads/{filename}',
            file_obj
        )
        
        file_obj.seek(0)
        return send_file(
            file_obj,
            download_name=filename,
            as_attachment=True
        )
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/files')
def list_files():
    """
    List files in S3 bucket
    
    Benefits over PHP:
    1. Pagination support
    2. Rich metadata
    3. Search capabilities
    """
    try:
        s3_client = get_s3_client()
        
        # Get paginated results
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(
            Bucket=os.getenv('AWS_BUCKET_NAME'),
            Prefix='uploads/'
        )
        
        files = []
        for page in page_iterator:
            for obj in page.get('Contents', []):
                # Get object metadata
                response = s3_client.head_object(
                    Bucket=os.getenv('AWS_BUCKET_NAME'),
                    Key=obj['Key']
                )
                
                files.append({
                    'name': obj['Key'].split('/')[-1],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'metadata': response.get('Metadata', {})
                })
                
        return jsonify({'files': files})
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """
    Delete file from S3
    
    Benefits over PHP:
    1. Versioning support
    2. Soft deletes
    3. Audit trail
    """
    try:
        s3_client = get_s3_client()
        
        s3_client.delete_object(
            Bucket=os.getenv('AWS_BUCKET_NAME'),
            Key=f'uploads/{filename}'
        )
        
        return jsonify({'message': 'File deleted successfully'})
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

# SQS Message Queue Operations
def get_sqs_client():
    """Get SQS client for message queuing"""
    return boto3.client('sqs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

@app.route('/queue/send', methods=['POST'])
def send_message():
    """
    Send message to SQS queue
    Not possible with basic PHP!
    """
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
            
        sqs_client = get_sqs_client()
        
        response = sqs_client.send_message(
            QueueUrl=os.getenv('AWS_QUEUE_URL'),
            MessageBody=json.dumps(message),
            MessageAttributes={
                'MessageType': {
                    'DataType': 'String',
                    'StringValue': 'UserMessage'
                }
            }
        )
        
        return jsonify({
            'message': 'Message sent',
            'message_id': response['MessageId']
        })
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/queue/receive')
def receive_messages():
    """Receive messages from SQS queue"""
    try:
        sqs_client = get_sqs_client()
        
        response = sqs_client.receive_message(
            QueueUrl=os.getenv('AWS_QUEUE_URL'),
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
            MessageAttributeNames=['All']
        )
        
        messages = []
        for message in response.get('Messages', []):
            # Process message
            messages.append({
                'id': message['MessageId'],
                'body': json.loads(message['Body']),
                'attributes': message.get('MessageAttributes', {})
            })
            
            # Delete processed message
            sqs_client.delete_message(
                QueueUrl=os.getenv('AWS_QUEUE_URL'),
                ReceiptHandle=message['ReceiptHandle']
            )
            
        return jsonify({'messages': messages})
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

# SNS Notification Operations
def get_sns_client():
    """Get SNS client for notifications"""
    return boto3.client('sns',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

@app.route('/notify', methods=['POST'])
def send_notification():
    """
    Send SNS notification
    More powerful than PHP mail()
    """
    try:
        message = request.json.get('message')
        subject = request.json.get('subject', 'Notification')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
            
        sns_client = get_sns_client()
        
        response = sns_client.publish(
            TopicArn=os.getenv('AWS_SNS_TOPIC_ARN'),
            Message=json.dumps({
                'default': message,
                'email': message,  # Email format
                'sms': message[:140]  # SMS format
            }),
            Subject=subject,
            MessageStructure='json'
        )
        
        return jsonify({
            'message': 'Notification sent',
            'message_id': response['MessageId']
        })
        
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

# Best Practices

"""
1. S3 Best Practices:
   - Use appropriate storage class
   - Implement bucket policies
   - Enable versioning
   - Configure lifecycle rules
   - Use presigned URLs

Example of presigned URL:
```python
def generate_presigned_url(filename, expiration=3600):
    s3_client = get_s3_client()
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.getenv('AWS_BUCKET_NAME'),
                'Key': f'uploads/{filename}'
            },
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        return None
```

2. SQS Best Practices:
   - Use dead-letter queues
   - Handle message deduplication
   - Implement retry logic
   - Monitor queue metrics
   - Use batch operations

3. SNS Best Practices:
   - Use topic filtering
   - Implement error handling
   - Monitor delivery status
   - Use message attributes
   - Consider message format

4. Security:
   - Use IAM roles
   - Implement least privilege
   - Enable encryption
   - Monitor AWS CloudTrail
   - Regular security audits

5. Error Handling:
```python
def aws_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            app.logger.error(f"AWS Error: {error_code} - {error_message}")
            return jsonify({
                'error': 'AWS operation failed',
                'details': error_message
            }), 500
    return wrapper
```

6. Configuration Management:
```python
class AWSConfig:
    def __init__(self):
        self.s3_client = None
        self.sqs_client = None
        self.sns_client = None
        
    def get_s3_client(self):
        if not self.s3_client:
            self.s3_client = boto3.client('s3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION')
            )
        return self.s3_client
```

7. Monitoring and Logging:
```python
def setup_aws_logging():
    import logging
    
    # Set up CloudWatch logging
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group='FlaskAppLogs',
        stream_name='AppLogs',
        boto3_client=boto3.client('logs')
    )
    
    app.logger.addHandler(cloudwatch_handler)
    app.logger.setLevel(logging.INFO)
```
"""

if __name__ == '__main__':
    app.run(debug=True)
