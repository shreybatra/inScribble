import logging

import azure.functions as func
from pymongo import MongoClient
from ..common.response import make_response
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Sign Up function processed a request.")

    body = req.get_json()

    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-cty3m.azure.mongodb.net:27017,cluster0-shard-00-01-cty3m.azure.mongodb.net:27017,cluster0-shard-00-02-cty3m.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    )
    db = client["inscribble"]
    users = db["users"]

    if (
        not body.get("email")
        or not body.get("password")
        or not body.get("name")
        or not body.get("role")
    ):
        return make_response({"msg": "Information is missing"}, 400)
    else:
        check_user = users.find_one({"email": body["email"]})

        if check_user:
            return make_response(
                {"msg": "User already there. Try different email."}, 409
            )
        else:
            users.insert_one(
                {
                    "name": body["name"],
                    "email": body["email"],
                    "password": body["password"],
                    "role": body["role"],
                }
            )

            return make_response({"msg": "Sign Up successful."}, 200)

