from agency_swarm.agents import Agent
from .tools.TaskCoordination import TaskCoordination
from .tools.ProgressMonitor import ProgressMonitor
from .tools.DecisionSupport import DecisionSupport
from agencii_connector import AgenciiConnector

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ManagerAgent",
            description="Central coordinator and decision maker for the agency",
            instructions="./instructions.md",
            tools=[TaskCoordination, ProgressMonitor, DecisionSupport],
            temperature=0.7
        )
        self.agencii = AgenciiConnector()
        self.active_chat_id = None

    def process_message(self, message, chat_id=None):
        if not self.active_chat_id:
            self.active_chat_id = self.agencii.create_chat()
        return self.agencii.send_message(message, self.active_chat_id)