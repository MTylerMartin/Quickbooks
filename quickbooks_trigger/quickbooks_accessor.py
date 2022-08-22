import json
import os
from intuitlib.client import AuthClient
import cglogging as cgl
import requests
from constants import client_secrets, qBData


logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()

auth_client = AuthClient(
        client_id=client_secrets.client_id,
        client_secret=client_secrets.client_secret,
        access_token=qBData.accessToken,  # If you do not pass this in, the Quickbooks client will call refresh and get a new access token.
        environment=client_secrets.environment,
        redirect_uri=client_secrets.redirect_uri,
    )


