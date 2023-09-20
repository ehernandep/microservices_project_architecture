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


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def handler(event, context):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM terraindetails""")
        columns = [desc[0] for desc in cursor.description]
        terrain_data_arr = [dict(zip(columns, row)) for row in cursor.fetchall()]

    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM partitionedterrains""")
        columns = [desc[0] for desc in cursor.description]
        partitioned_terrain_arr = [dict(zip(columns, row)) for row in cursor.fetchall()]

    terrain_mapping = {}
    for item in partitioned_terrain_arr:
        terrain_id = item["terrain_id"]
        if terrain_id not in terrain_mapping:
            terrain_mapping[terrain_id] = []
        terrain_mapping[terrain_id].append(
            {
                "partitioned_terrain_id": item["partitioned_terrain_id"],
                "terrain_id": terrain_id,
                "partition_area": item["partition_area"],
            }
        )

    for item in terrain_data_arr:
        terrain_id = item["terrain_id"]
        if terrain_id in terrain_mapping:
            item["partitioned_terrain"] = terrain_mapping[terrain_id]
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(terrain_data_arr, indent=4, cls=DecimalEncoder),
    }
