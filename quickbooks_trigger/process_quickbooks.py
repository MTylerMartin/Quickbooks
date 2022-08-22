import cglogging as cgl
import os
import json
from secret_manager import secret_manager
from Message import Message
from lambda_accessor import lambda_accessor
from datetime import datetime

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def process_message(request):
    logger.debug("inside trigger event")
    logger.debug(request)
    message = Message()
    response_message = request["eventResponse"]["responseMessage"][0]

    # determine if trip type is not training or maintenance
    if response_message["orderDetail"]["tripDetail"]["charterTripType"] == 86 or \
            response_message["orderDetail"]["tripDetail"]["charterTripType"] == 99:
        logger.debug("Skipping: Trip Type not valid")
        return message.get_good_standard_message()

    if response_message["orderStatus"] != "CLOSED":
        logger.debug("Skipping: Order Status not CLOSED")
        return message.get_good_standard_message()

    # get z token
    return_code, return_type, secret_token = secret_manager.get_secrets(os.environ.get("CAG_ZA_TOKEN"))
    if return_code != 0:
        logger.debug(message.get_fatal_standard_message(return_code))
        return message.get_good_standard_message()
    token = json.loads(secret_token['SecretString'])['JWT']

    # access business profile microservice (API Call)
    return_code, error_message, read_business_profile = \
        lambda_accessor.call_businessProfile(build_read_business_profile(response_message["supplierId"], token))
    if return_code != 0:
        logger.debug(message.get_fatal_standard_message(return_code))
        return message.get_good_standard_message()

    # checked business profile for supplier profile (not broker profile)
    for profile in read_business_profile["responseMessage"]:
        if profile["businessProfileId"] == 0 and "profileType" in profile and profile["profileType"].upper() == "SP":
            business_profile = profile
            break

    

    # getting login credentials for Quickbooks API
    return_code, return_type, secret_token = secret_manager.get_secrets(os.getenv("CAG_ZA_TOKEN"))
    if return_code != 0:
        return message.get_fatal_standard_message(return_code)
    # extracting api key from secret
    account = json.loads(secret_token['SecretString'])


def build_read_business_profile(supplier, token):
    return {
        "context": {
            "domainName": "BusinessProfile",
            "securityToken": token,
            "language": "EN"
        },
        "commonParms": {
            "action": "READ",
            "view": "DEFAULT",
            "version": "1.0.0",
            "transactionId": "PETERG ACCOUNTS"
        },
        "request": {
            "supplierId": supplier
        }
    }

def create_invoice_json(create_date, cost_calculated, ):
    return {
      "Invoice": {
        "TxnDate": create_date,
        "domain": "QBO",
        "PrintStatus": "NeedToPrint",
        "SalesTermRef": {
          "value": "3"
        },
        "TotalAmt": cost_calculated,
        "Line": [
          {
            "Description": "Aircraft Flight Fee",
            "DetailType": "SalesItemLineDetail",
            "SalesItemLineDetail": {
              "TaxCodeRef": {
                "value": "TAX"
              },
              "Qty": 1,
              "UnitPrice": 1,
              "ItemRef": {
                "name": "Rock Fountain",
                "value": "5"
              }
            },
            "LineNum": 1,
            "Amount": 275.0,
            "Id": "1"
          }