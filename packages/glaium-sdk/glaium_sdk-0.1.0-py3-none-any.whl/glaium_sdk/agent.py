import logging
from .client import GlaiumClient
from .client import BadRequestError, ApiError, NetworkError
from typing import List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Creates Agent and gets organization's goal
class Agent:
    def __init__(self, auth_token: str):
        self.client = GlaiumClient(auth_token)

    
    def create(self, name: str, description: str, inputs: List[str], output_freq: str) -> int:

        if not name or not inputs or not output_freq or not description:
            raise BadRequestError("Missing required parameters")
        
        data = {
            "name": name,
            "inputs": inputs,
            "output_freq": output_freq,
            "description": description
        }

        try:
            response = self.client._request("POST", "/agent/", data=data)
            if response["status"] == 200:
                agent_id = response["agent_id"]
                logger.info(f"Successfully created Agent with id {agent_id}")
                return agent_id
            else:
                logger.error(f"Failed to create Agent: {response}")
                raise ApiError("Error while creating Agent")
            
        except (ApiError, NetworkError) as e:
            logger.error("Error setting goals: %s", str(e))
            return False


    def get_goals(self, agent_id: int):

        if not agent_id:
            raise BadRequestError("Missing required parameters: 'agent_id'.")

        endpoint = f"/agent/{agent_id}"

        try:
            response = self.client._request("GET", endpoint=endpoint)

            if response.get("status") == 200:
                logger.info(f"Agent's goals with id {agent_id} is being fetched")
                return response
            else:
                logger.error(f"Failed to retrieve goals for agent {agent_id}")
                raise ApiError("Error while fetching Agent's goals")

        except (ApiError, NetworkError) as e:
            logger.error("Error setting goals: %s", str(e))
            return False