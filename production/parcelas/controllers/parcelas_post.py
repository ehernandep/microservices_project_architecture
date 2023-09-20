import os
import psycopg2
import json
import uuid

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


def _create_terrain_details(user_id, terrain_name, terrain_area, partition_count):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO terraindetails (user_id, terrain_name, terrain_area, partition_count)
            VALUES (%s, %s, %s, %s) RETURNING terrain_id;
            """
        cursor.execute(query, (user_id, terrain_name, terrain_area, partition_count))
        terrain_id = cursor.fetchone()[0]
        conn.commit()
    return terrain_id


def _create_terrain_partitions(partition_count, terrain_id, terrain_division_area):
    for i in range(partition_count):
        with conn.cursor() as cursor:
            query = """
                INSERT INTO partitionedterrains (terrain_id, partition_area)
                VALUES (%s, %s);
                """
            cursor.execute(query, (terrain_id, terrain_division_area))
            conn.commit()


def handler(event, context):
    event_body = json.loads(event['body'])
    print(event_body)
    user_id = str(uuid.uuid4().hex)
    terrain_name = event_body['terrain_name']
    terrain_area = event_body['terrain_area']
    partition_count = event_body['partition_count']
    terrain_id = _create_terrain_details(
        user_id, terrain_name, terrain_area, partition_count
    )
    terrain_division_area = terrain_area / partition_count
    _create_terrain_partitions(partition_count, terrain_id, terrain_division_area)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": "Success",
    }
