import os
import psycopg2
import json
from decimal import Decimal

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


# en el front terrain_name-partitionedterrain_id para identificar
def handler(event, context):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM followingpartitionedterrain""")
        columns = [desc[0] for desc in cursor.description]
        following_partition_terrain = [
            dict(zip(columns, row)) for row in cursor.fetchall()
        ]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(following_partition_terrain),
    }
