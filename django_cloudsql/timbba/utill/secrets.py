"""
    This file contains class to intract with google cloud to get secrete information from google cloud secrete manager.
"""
import logging
from google.cloud import secretmanager
import os

logging.basicConfig(level=logging.DEBUG)

class SecretManager:
    """
        This class make connection with google cloud secrete manager and get secretes.
    """
    def __init__(self, project_id, secret_id):
        self.project_id = project_id
        self.secret_id = secret_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self):
        """
        This function intract with google cloud secrete manager with projectid,secreteid and google cloud credential file to get the secrete's values.

        returns:
            dictionary:function return dictionary which contains database password,database name,database user.
        """
        # assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"

        secret_name = f"projects/{self.project_id}/secrets/{self.secret_id}/versions/latest"

        response = self.client.access_secret_version(name=secret_name)

        secret_payload = response.payload.data.decode("UTF-8")

        logging.debug(f"Secret value: {secret_payload}")

        return secret_payload
