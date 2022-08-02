import json
import os
import datetime
import boto3
from botocore.exceptions import ClientError

import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()
user = ""
password = ""


class secret_manager:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.environ.get("CAG_REGION")
    )

    @classmethod
    def get_secrets(cls, key_name):
        logger.debug("inside getSecrets")

        errNum, errMsg, secret = 0, '', None

        try:
            get_secret_value_response = cls.client.get_secret_value(
                SecretId=key_name
            )
            return 0, " ", get_secret_value_response
        except ClientError as e:
            logger.debug('Unexpected error: {0}'.format(e))
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                return 8089, 'DecryptionFailureException', secret
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                return 8089, 'InternalServiceErrorException', secret
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                return 8089, 'InvalidParameterException', secret
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                return 8089, 'InvalidRequestException', secret
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                return 8088, 'ResourceNotFoundException', secret

    @classmethod
    def create_secret(cls, name):
        try:
            errNum, errMsg, = 0, '',
            kwargs = {'Name': name, 'SecretString': "initialize"}
            response = cls.client.create_secret(**kwargs)
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return 0, "GOOD", response
        except ClientError:
            return 1, "Couldn't create secret", " "

    @classmethod
    def update_secret(cls, name, secret_dictionary):
        try:
            newSecret = json.dumps(secret_dictionary)
            kwargs = {'SecretId': name}
            if isinstance(newSecret, str):
                kwargs['SecretString'] = newSecret
            elif isinstance(newSecret, bytes):
                kwargs['SecretBinary'] = newSecret
            response = cls.client.put_secret_value(**kwargs)
        except ClientError:
            return 1, "Fatal"
        else:
            return 0, "Good"

    @classmethod
    def add_secret(cls, secret, request):
        values = {}
        payload = {"account": "Wyvern",
                   "userName": request["request"]["userName"],
                   "password": request["request"]["password"],
                   "status": "active",
                   "type": "safetyRating",
                   "lastUpdated": format(datetime.datetime.utcnow()),
                   "token": []}
        key = str(payload["userName"]) + "-" + str(payload["account"])
        if secret["SecretString"] == "initialize":
            values[key] = json.dumps(payload)
        else:
            values = json.loads(secret["SecretString"])
            if key in values:
                return 10, "duplicate", " "
            values[key] = json.dumps(payload)
        try:
            newSecret = json.dumps(values)
            kwargs = {'SecretId': secret["Name"]}
            if isinstance(newSecret, str):
                kwargs['SecretString'] = newSecret
            elif isinstance(newSecret, bytes):
                kwargs['SecretBinary'] = newSecret
            response = cls.client.put_secret_value(**kwargs)
        except ClientError:
            return 1, "exception", " "
        else:
            return 0, response, key