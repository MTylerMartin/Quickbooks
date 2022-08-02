import json
import Message
import cglogging as cgl


logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def lambda_handler(event, context):
    logger.debug(event)
    message = Message.Message()
    response = {}
    logger.debug("Received event: ")
    try:
        if "Records" in event:
            for record in event["Records"]:
                if "body" not in record:
                    message.get_good_standard_message(1)

                if "Message" not in record["body"]:
                    return return_response(message.get_good_standard_message())

                body = json.loads(record["body"])
                trigger_message = json.loads(body["Message"])

                if "eventRequest" not in trigger_message:
                    return return_response(message.get_good_standard_message())

                if trigger_message["domain"].upper() == "order".upper():
                    if "eventResponse" not in trigger_message:
                        return return_response(message.get_good_standard_message())
                    if trigger_message["eventResponse"]["standardResponse"]["returnCode"] != 0:
                        return_response(message.get_good_standard_message())
                    logger.debug(trigger_message)

                #     response = RequestRouter.router("trigger", trigger_message)
                # else:
                #     response = RequestRouter.router(trigger_message["domain"], trigger_message)
            logger.debug(response)
        return return_response(response)

    except Exception as details:
        logger.debug("in app level exception")
        logger.debug(details)
        return return_response(" ")


def return_response(response):
    logger.debug("in app level exception")
    transactionResponse = {'statusCode': '200', 'headers': {}}
    transactionResponse['headers']['Content - Type'] = 'applicationjson'
    transactionResponse['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,PUT,PATCH'
    transactionResponse['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
    transactionResponse['headers']['Access-Control-Allow-Origin'] = '*'
    transactionResponse['headers']['Access-Control-Allow-Credentials'] = True
    transactionResponse['body'] = json.dumps(response)
    logger.debug("Transaction Response: {}".format(transactionResponse))
    return transactionResponse