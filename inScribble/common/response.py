import json
import azure.functions as func


def make_response(response, status_code=200):

    response = str(json.dumps(response))

    return func.HttpResponse(
        response,
        headers={"Content-Type": "application/json"},
        status_code=status_code,
    )
