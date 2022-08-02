import json
import os

import boto3
import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class lambda_accessor:
    lambda_client = boto3.client("lambda", region_name=os.environ.get("CAG_REGION"))
    functionName = " "

    @classmethod
    def call_userprofile(self, request):
        self.functionName = os.getenv("CAG_USER_PROFILE")
        return_code, return_type, response = self.call_lambda(request)
        logger.debug("done with Crew")
        return return_code, return_type, response

    @classmethod
    def call_businessProfile(self, request):
        logger.debug(request)
        self.functionName = os.getenv("CAG_BUSINESS_PROFILE_FUNCTION")
        return_code, return_type, response = self.call_lambda(request)
        logger.debug(response)
        return return_code, return_type, response

    @classmethod
    def call_AccountPluginManger(self, request):
        logger.debug(request)
        self.functionName = os.getenv("CAG_ACCOUNT_PLUGIN_MANAGER_FUNCTION")
        return_code, return_type, response = self.call_lambda(request)
        logger.debug(response)
        return return_code, return_type, response

    @classmethod
    def call_AircraftSpecification(self, request):
        logger.debug(request)
        self.functionName = os.getenv("CAG_AIRCRAFT")
        return_code, return_type, response = self.call_lambda(request)
        logger.debug(response)
        return return_code, return_type, response

    @classmethod
    def call_orders(self, request):
        logger.debug(request)
        self.functionName = os.getenv("CAG_ORDERS")
        return_code, return_type, response = self.call_lambda(request)
        logger.debug(response)
        return return_code, return_type, response



    @classmethod
    def call_lambda(self, payload):
        try:
            test = json.dumps(payload)
            response = self.lambda_client.invoke(
                FunctionName=self.functionName,
                InvocationType="RequestResponse",
                LogType='None',
                Payload=json.dumps(payload),
            )

            #  does response contain payload element
            if 'Payload' not in response:
                if self.functionName == os.getenv("CAG_CREW_FUNCTION"):
                    return 44005, " ", " "
                else:
                    return 44006, " ", " "
            if 'StatusCode' not in response or response['StatusCode'] != 200:
                if self.functionName == os.getenv("CAG_CREW_FUNCTION"):
                    return 44005, " ", " "
                else:
                    return 44006, " ", " "

            jsonString = response['Payload'].read()

            #  validate json response
            if len(jsonString) <= 0:
                if self.functionName == os.getenv("CAG_CAMP_FUNCTION"):
                    return 33007, "FATAL", "Invalid JSON in payload"
                else:
                    return 33008, "FATAL", " "

            responseObj = json.loads(jsonString)
            logger.debug("JSON String Response from profile: {}".format(responseObj))
            # add message validation on the response and take error
            if "body" in responseObj:
                body = json.loads(responseObj["body"])
                if "standardresponse" in body:
                    body['standardResponse'] = body["standardresponse"]
                if 'standardResponse' not in body:
                    return 1, "FATAL", "No standard response element in response from profiles"

                if body['standardResponse']['returnCode'] != 0:
                    return body['standardResponse']['returnCode'], "FATAL", body['standardResponse']
                return 0, "GOOD", body

            if 'standardResponse' not in responseObj:
                return 33011, "FATAL", "No standard response element in response from profiles"

            if responseObj['standardResponse']['returnCode'] != 0:
                return responseObj['standardResponse']['returnCode'], "FATAL", responseObj

            return 0, "GOOD", responseObj

        except Exception as details:
            logger.error('Unexpected error: {0}'.format(details))
            return 1, "FATAL", "Exception, retrieving supplier profiles"