import os
import psycopg2


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
    cursor.execute(
        """INSERT INTO example (name, age)
            VALUES ('s', 23);"""
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"statusCode": 200, "body": "Connected to the database successfully!"}
