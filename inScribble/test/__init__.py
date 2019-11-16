import logging
from ..common.response import make_response
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    return make_response({"msg": "Service is working fine. App is up."})
