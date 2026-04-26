import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = "rohit-file-upload-unique123"
TABLE_NAME = "file_metadata"

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.jpg"

        # Generate upload URL
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_name,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=300
        )

        # Save metadata in DynamoDB
        table.put_item(
            Item={
                "file_id": file_id,
                "file_name": file_name,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "uploadURL": upload_url,
                "file_id": file_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": str(e)
        }
