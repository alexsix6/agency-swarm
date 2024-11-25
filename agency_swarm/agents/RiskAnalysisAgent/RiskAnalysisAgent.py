from agency_swarm.agents import Agent
from .tools.RiskEvaluator import RiskEvaluator
from .tools.MitigationPlanner import MitigationPlanner
from .tools.SafetyReporter import SafetyReporter
from agencii_connector import AgenciiConnector

class RiskAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RiskAnalysisAgent",
            description="Physical risk assessment specialist",
            instructions="./instructions.md",
            tools=[RiskEvaluator, MitigationPlanner, SafetyReporter],
            temperature=0.7
        )
        self.agencii = AgenciiConnector()
        self.active_chat_id = None

    def process_message(self, message, chat_id=None):
        if not self.active_chat_id:
            self.active_chat_id = self.agencii.create_chat()
        return self.agencii.send_message(message, self.active_chat_id)