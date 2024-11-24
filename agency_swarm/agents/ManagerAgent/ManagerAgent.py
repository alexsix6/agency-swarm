from agency_swarm.agents import Agent
from .tools.TaskCoordination import TaskCoordination
from .tools.ProgressMonitor import ProgressMonitor
from .tools.DecisionSupport import DecisionSupport

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ManagerAgent",
            description="Central coordinator and decision maker for the agency",
            instructions="./instructions.md",
            tools=[TaskCoordination, ProgressMonitor, DecisionSupport],
            temperature=0.7
        )