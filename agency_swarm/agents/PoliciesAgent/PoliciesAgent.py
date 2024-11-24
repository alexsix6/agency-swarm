from agency_swarm.agents import Agent
from .tools.DocumentSearch import DocumentSearch
from .tools.PolicyAnalyzer import PolicyAnalyzer
from .tools.ComplianceChecker import ComplianceChecker

class PoliciesAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PoliciesAgent",
            description="Corporate policy and regulation expert",
            instructions="./instructions.md",
            tools=[DocumentSearch, PolicyAnalyzer, ComplianceChecker],
            temperature=0.6
        )