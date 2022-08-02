import json
import datetime


class Message:

    def __init__(self):
        self.dictionary = {0: " ",
                           44001: "Error: Failed to login.",
                           44002: "Error: Failed to update trip in flightBridge",
                           8090: " bad token",
                           8093: " bad token",
                           39002: "account already exsists",
                           2: "Exception, Unexpected error Auto Close Handler",
                           19002: "Exception, Unexpected error",
                           10: "duplicate account",
                           23003: " Exception, invalid token"
                           }
        self.message = {"standardResponse": {}, "responseMessage": {}}
        self.warnings = {"warnings": []}

    def add_warnings(self, warning):
        self.warnings["warnings"].append(warning)

    def get_response(self, err_num, response):

        if err_num == 0:
            self.message["standardResponse"] = self.get_good_standard_message()["standardResponse"]
            self.message["responseMessage"] = response
            print(json.dumps(self.message))
            return self.message

        else:
            self.message["standardResponse"] = self.get_fatal_standard_message(err_num)["standardResponse"]
            self.message["responseMessage"] = response
            print(json.dumps(self.message))
            return self.message

    def get_good_standard_message(self):
        return {
            "standardResponse": {
                "count": 0,
                "domain": "FlightBridgeTrigger",
                "errorMessage": "",
                "language": "EN",
                "responseType": "GOOD",
                "returnCode": 0,
                "timeStampOfMessage": format(datetime.datetime.utcnow()),
                "warnings": self.warnings["warnings"]
            }
        }

    def get_fatal_standard_message(self, err_num):
        return {
            "standardResponse": {
                "count": 0,
                "domain": "ForeFlightBroker",
                "errorMessage": self.dictionary[err_num],
                "language": "EN",
                "responseType": "FATAL",
                "returnCode": err_num,
                "timeStampOfMessage": format(datetime.datetime.utcnow()),
                "warnings": self.warnings["warnings"]
            }
        }