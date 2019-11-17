import logging

import azure.functions as func
from ..common.response import make_response
from pymongo import MongoClient
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    body = req.get_json()

    if not (
        body.get("doctorEmail")
        and body.get("patientEmail")
        and body.get("medications")
    ):
        return make_response(
            {"msg": "Information missing. (email both, medications)"}, 400
        )

    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-cty3m.azure.mongodb.net:27017,cluster0-shard-00-01-cty3m.azure.mongodb.net:27017,cluster0-shard-00-02-cty3m.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    )

    db = client["inscribble"]
    prescriptions = db["prescriptions"]

    body["createdOn"] = datetime.now()

    prescriptions.insert_one(body)

    return make_response({"msg": "Inserted successfully."}, 201)
