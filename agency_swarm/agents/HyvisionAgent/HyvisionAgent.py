from agency_swarm.agents import Agent
from .tools.TechnicalDocManager import TechnicalDocManager
from .tools.SystemDiagnostics import SystemDiagnostics
from .tools.SupportAssistant import SupportAssistant

class HyvisionAgent(Agent):
    def __init__(self):
        super().__init__(
            name="HyvisionAgent",
            description="Hyvision software technical specialist",
            instructions="./instructions.md",
            tools=[TechnicalDocManager, SystemDiagnostics, SupportAssistant],
            temperature=0.6
        )