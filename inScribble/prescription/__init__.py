import logging
import requests
import json

from ..common.response import make_response
from .extract import extract_info
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Submit Function processed a request.")

    body = req.get_json()

    print(type(body))

    logging.info("######################" + str(body))

    url = "https://inscribble.cognitiveservices.azure.com/inkrecognizer/v1.0-preview/recognize"

    response = requests.put(
        url=url,
        data=json.dumps(body),
        headers={
            "Ocp-Apim-Subscription-Key": "3f296778686f4a91a5cb3e540c9ee57f",
            "Content-Type": "application/json",
        },
    )
    if response.status_code == 200:
        logging.info("######################" + str(response.json()))

        result = extract_info(response.json())
        for doc in result:
            if doc["count"] == 0:
                doc["frequency"] = "Once a day."
            elif doc["count"] == 1:
                doc["frequency"] = "Once a day."
            elif doc["count"] == 2:
                doc["frequency"] = "2 times in a day."
            elif doc["count"] == 3:
                doc["frequency"] = "3 times in a day."
            elif doc["count"] > 3:
                doc["frequency"] = "Multiple times."
            doc.pop("count")

        return make_response(result, 201)
    else:
        logging.info("######################" + str(response.content))
        return make_response({"msg": "Internal Error"}, 500)

