import json
import os

import Message
import cglogging as cgl
import process_flight_bridge
import process_webhook

from action_enum import action_enum

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class RequestRouter:
    """Routes the request"""

    @classmethod
    def router(cls, action, request):
        """ Routes the request based on the action. Depending on the action, it will perform the action and return a
        response payload """

        logger.debug("inside router")
        if action.upper() == action_enum.Trigger.name.upper():
            logger.debug("at trigger")
            response = process_flight_bridge.process_trigger_event(request["eventResponse"]["responseMessage"])
        if action.upper() == action_enum.FlightBridgeWebHook.name.upper():
            response = process_webhook.precess_message(request["eventRequest"])

        return response