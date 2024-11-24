from agency_swarm.agents import Agent
from .tools.BigQueryConnector import BigQueryConnector
from .tools.DataVisualizer import DataVisualizer
from .tools.StatisticalAnalyzer import StatisticalAnalyzer

class StatisticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="StatisticsAgent",
            description="Data analysis and insights generator using BigQuery",
            instructions="./instructions.md",
            tools=[BigQueryConnector, DataVisualizer, StatisticalAnalyzer],
            temperature=0.7
        )