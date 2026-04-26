import json
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "rohit-file-upload-unique123"

def lambda_handler(event, context):
    try:
        # Get query params
        params = event.get("queryStringParameters")

        if not params or "file_id" not in params:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": "file_id is required"
            }

        file_id = params["file_id"]
        file_name = f"{file_id}.jpg"

        # Generate download URL
        download_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_name
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "downloadURL": download_url
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
