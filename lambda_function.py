import json
import pymysql

def lambda_handler(event, context):
    # Database connection details
    endpoint = "my-aurora-cluster.cluster-xxxxxx.us-east-1.rds.amazonaws.com"
    username = "admin"
    password = "your-password"
    database_name = "your-database-name"

    # Connect to the database
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    cursor = connection.cursor()

    # Parse the HTTP method and body
    http_method = event['httpMethod']
    body = json.loads(event['body']) if 'body' in event else {}

    # Perform CRUD operations
    if http_method == 'GET':
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        response = {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    elif http_method == 'POST':
        name = body['name']
        email = body['email']
        cursor.execute(f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')")
        connection.commit()
        response = {
            'statusCode': 201,
            'body': json.dumps({'message': 'User created successfully'})
        }
    elif http_method == 'DELETE':
        user_id = body['id']
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        connection.commit()
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    else:
        response = {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid HTTP method'})
        }

    # Close the database connection
    cursor.close()
    connection.close()

    return response