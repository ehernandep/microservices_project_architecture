import os
import psycopg2
import json

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


def _create_following_partitioned_terrain(
    partitionedterrain_id, product_name, sowing_date, harvest_date, details, terrain_id
):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO followingpartitionedterrain (partitionedterrain_id, product_name, sowing_date, harvest_date, details, terrain_id)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
        cursor.execute(
            query,
            (
                partitionedterrain_id,
                product_name,
                sowing_date,
                harvest_date,
                details,
                terrain_id,
            ),
        )
        conn.commit()


def handler(event, context):
    event_body = json.loads(event["body"])
    _create_following_partitioned_terrain(**event_body)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": "successfully created",
    }
