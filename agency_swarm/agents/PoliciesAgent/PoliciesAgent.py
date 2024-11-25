from agency_swarm.agents import Agent
from .tools.DocumentSearch import DocumentSearch
from .tools.PolicyAnalyzer import PolicyAnalyzer
from .tools.ComplianceChecker import ComplianceChecker
from agencii_connector import AgenciiConnector

class PoliciesAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PoliciesAgent",
            description="Corporate policy and regulation expert",
            instructions="./instructions.md",
            tools=[DocumentSearch, PolicyAnalyzer, ComplianceChecker],
            temperature=0.6
        )
        self.agencii = AgenciiConnector()
        self.active_chat_id = None

    def process_message(self, message, chat_id=None):
        if not self.active_chat_id:
            self.active_chat_id = self.agencii.create_chat()
        return self.agencii.send_message(message, self.active_chat_id)