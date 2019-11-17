import logging

import azure.functions as func
from ..common.response import make_response
from pymongo import MongoClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    email = req.params.get("email")

    if not email:
        return make_response({"msg": "Email not sent."}, 400)

    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-cty3m.azure.mongodb.net:27017,cluster0-shard-00-01-cty3m.azure.mongodb.net:27017,cluster0-shard-00-02-cty3m.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    )

    db = client["inscribble"]
    prescriptions = db["prescriptions"]

    result = list(
        prescriptions.aggregate(
            [
                {"$match": {"patientEmail": email}},
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
                    }
                },
                {"$unwind": "$name"},
            ]
        )
    )

    for doc in result:
        doc["id"] = str(doc.pop("_id"))
        doc["createdOn"] = int(doc["createdOn"].timestamp() * 1000)

    return make_response({"data": result}, 200)

