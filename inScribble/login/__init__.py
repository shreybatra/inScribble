import logging

import azure.functions as func
from ..common.response import make_response
from pymongo import MongoClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    body = req.get_json()

    if not (body.get("email") and body.get("password")):
        return make_response({"msg": "Email or password missing."}, 400)

    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-cty3m.azure.mongodb.net:27017,cluster0-shard-00-01-cty3m.azure.mongodb.net:27017,cluster0-shard-00-02-cty3m.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    )

    db = client["inscribble"]
    users = db["users"]

    doc = users.find_one({"email": body["email"], "password": body["password"]})

    if doc:
        doc.pop("_id")
        # logging.info(doc)
        return make_response({"msg": "Login sucessful.", "data": doc}, 200)

    else:
        return make_response({"msg": "Invalid Email or Password."}, 400)
