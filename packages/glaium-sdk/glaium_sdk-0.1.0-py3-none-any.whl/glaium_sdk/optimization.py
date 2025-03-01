import logging
from datetime import datetime
from typing import Union
from .client import GlaiumClient
from .client import AuthenticationError, BadRequestError, AuthenticationError, ApiError, NetworkError


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Optimization:
    def __init__(self, access_token: str):
        self.client = GlaiumClient(access_token) 
        self.auth_token = None   

    def authenticate(self, username: str, password: str, access_token: str) -> str:
        if not username or not password or not access_token:
            raise BadRequestError("Missing required parameters")
        
        try:
            data = {
                "username": username,
                "password": password,
                "token": access_token
            }

            logger.info(f"AUTHENTICATE SDK DATA: {data}")

            response = self.client._request("POST", "/authenticate/", data=data)

            logger.info(f"RESPONSE: {response}")
            if response["status"] == 200:
                self.auth_token = response["auth_token"]
                self.client.session.headers.update(
                    {"Authorization": f"Bearer {self.auth_token}"}
                )
                return self.auth_token
            else:
                raise AuthenticationError("Failed to log in and generate API key")
        except (ApiError, NetworkError) as e:
            logger.error(f"Error authenticating user: {e}")

    def set_goals(self, target: str, outcome: str, by: Union[datetime, str]) -> bool:

        if not target or not outcome or not by:
            raise BadRequestError("Missing required parameters: 'target', 'outcome', or 'by'.")


        data = {
            "target": target,
            "outcome": outcome,
            "by": by
        }

        try:
            response = self.client._request("POST", "/goals/", data=data)

            logger.info(f"SET GOALS SDK DATA: {response}")

            if response["status"] == 200:
                logger.info(f"Successfully Set Goals: {response}")
                return True
            else:
                logger.error(f"Failed to Set Goals: {response}")
                return False
            
        except (ApiError, NetworkError) as e:
            logger.error("Error setting goals: %s", str(e))
            return False


    def run_pipeline(self, target: str, cycle: int):
        if not target or not cycle:
            raise BadRequestError("Missing required parameters")
        
        try:
            data = {
                "target": target,
                "cycle": cycle
            }

            logger.info(f"PIPELINE PARAMETERS: {data}")

            response = self.client._request("POST", '/run_pipeline/', data=data)

            if response["status"] == 200:
                logger.info(f"Successfully ran pipeline: {response}")
                return True
            else:
                logger.error(f"Failed to run pipeline: {response}")
                return False



        except (ApiError, NetworkError) as e:
            logger.error(f"Error running pipeline: {e}")
