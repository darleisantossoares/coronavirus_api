import json
import os
import sys

def api(handler, context):
    with open('database.json', 'r') as json_file:
        data = json.load(json_file)

    return {
            "statusCode": 200,
            "body": json.dumps(data),
            "headers": {
                "Access-Control-Allow-Origin": "*"
            }
        }


