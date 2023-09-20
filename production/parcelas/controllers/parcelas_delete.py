import os
import psycopg2
import json


def handler(event, context):
    rds_host = os.environ["DB_HOST"]
    rds_db_name = os.environ["DB_NAME"]
    rds_username = os.environ["DB_USER"]
    rds_password = os.environ["DB_PASSWORD"]
    conn = psycopg2.connect(
        host=rds_host,
        database=rds_db_name,
        user=rds_username,
        password=rds_password,
    )
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE TerrainDetails (
                    terrain_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    terrain_name VARCHAR(255),
                    terrain_area DECIMAL(10, 2),
                    partition_count INT);  """)
    cursor.commit()
    cursor.close()
    conn.close()


    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(data),
    }
