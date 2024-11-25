from agency_swarm.agents import Agent
from .tools.TechnicalDocManager import TechnicalDocManager
from .tools.SystemDiagnostics import SystemDiagnostics
from .tools.SupportAssistant import SupportAssistant
from agencii_connector import AgenciiConnector

class HyvisionAgent(Agent):
    def __init__(self):
        super().__init__(
            name="HyvisionAgent",
            description="Hyvision software technical specialist",
            instructions="./instructions.md",
            tools=[TechnicalDocManager, SystemDiagnostics, SupportAssistant],
            temperature=0.6
        )
        self.agencii = AgenciiConnector()
        self.active_chat_id = None

    def process_message(self, message, chat_id=None):
        if not self.active_chat_id:
            self.active_chat_id = self.agencii.create_chat()
        return self.agencii.send_message(message, self.active_chat_id)