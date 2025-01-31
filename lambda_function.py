import json
import boto3

client = boto3.client('rds-data')

DB_CLUSTER_ARN = "arn:aws:rds:us-east-1:123456789012:cluster:serverless-cluster"
DB_SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123456789012:secret:mydbsecret"
DATABASE_NAME = "mydatabase"

def execute_statement(sql):
    """Executes SQL queries on Aurora Serverless"""
    response = client.execute_statement(
        resourceArn=DB_CLUSTER_ARN,
        secretArn=DB_SECRET_ARN,
        database=DATABASE_NAME,
        sql=sql
    )
    return response

def lambda_handler(event, context):
    """Handles API Gateway requests"""
    try:
        if event['httpMethod'] == 'GET':
            sql = "SELECT * FROM users"
            result = execute_statement(sql)
            return {
                "statusCode": 200,
                "body": json.dumps(result['records'])
            }
        elif event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            name = body.get('name', '')
            sql = f"INSERT INTO users (name) VALUES ('{name}')"
            execute_statement(sql)
            return {
                "statusCode": 201,
                "body": json.dumps({"message": "User added successfully!"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
