import logging
from glaium_sdk.agent import Agent
from glaium_sdk.optimization import Optimization
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

optimization = Optimization(ACCESS_TOKEN)


auth_token = optimization.authenticate(USERNAME, PASSWORD, ACCESS_TOKEN)
logging.info(f"Auth Token: {auth_token}")


agent = Agent(auth_token)

optimization.run_pipeline("EngineeringBudget", 5)
# optimization.set_goals("HR Revenue", "> 100K", "2025-12-31")
# agent_id = agent.create("RandomAgent", "eeeeeee ", ["yyyyy"], "daily")

# logging.info(f"Agent ID: {agent_id}")


# optimization.run_mobile_app(cycle=10, target="TotalRevenue")
