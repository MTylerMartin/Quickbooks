import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def process_message(request):
    logger.debug(request)
    response_body = request[requestMessage]