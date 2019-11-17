import logging

import azure.functions as func
from ..common.response import make_response
from pymongo import MongoClient
from bson import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    prescription_id = req.params.get("prescriptionId")

    if not prescription_id:
        return make_response({"msg": "ID not sent."}, 400)

    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-cty3m.azure.mongodb.net:27017,cluster0-shard-00-01-cty3m.azure.mongodb.net:27017,cluster0-shard-00-02-cty3m.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    )

    db = client["inscribble"]
    prescriptions = db["prescriptions"]

    doc = list(
        prescriptions.aggregate(
            [
                {"$match": {"_id": ObjectId(prescription_id)}},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "doctorEmail",
                        "foreignField": "email",
                        "as": "member",
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "name": "$member.name",
                        "createdOn": 1,
                        "medications": 1,
                    }
                },
                {"$unwind": "$name"},
            ]
        )
    )

    if doc:
        doc = doc[0]
    else:
        doc = {}

    if not doc:
        return make_response({"msg": "ID not found."}, 404)

    doc["id"] = str(doc.pop("_id"))
    doc["createdOn"] = int(doc["createdOn"].timestamp() * 1000)

    return make_response({"data": doc})
