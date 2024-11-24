from agency_swarm.agents import Agent
from .tools.RiskEvaluator import RiskEvaluator
from .tools.MitigationPlanner import MitigationPlanner
from .tools.SafetyReporter import SafetyReporter

class RiskAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RiskAnalysisAgent",
            description="Physical risk assessment specialist",
            instructions="./instructions.md",
            tools=[RiskEvaluator, MitigationPlanner, SafetyReporter],
            temperature=0.7
        )