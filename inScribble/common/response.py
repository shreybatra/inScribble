import json
import azure.functions as func


def make_response(response):

    response = str(json.dumps(response))

    return func.HttpResponse(
        response, headers={"Content-Type": "application/json"}
    )
