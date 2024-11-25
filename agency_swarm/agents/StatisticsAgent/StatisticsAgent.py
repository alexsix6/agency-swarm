from agency_swarm.agents import Agent
from .tools.BigQueryConnector import BigQueryConnector
from .tools.DataVisualizer import DataVisualizer
from .tools.StatisticalAnalyzer import StatisticalAnalyzer
from agencii_connector import AgenciiConnector

class StatisticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="StatisticsAgent",
            description="Data analysis and insights generator using BigQuery",
            instructions="./instructions.md",
            tools=[BigQueryConnector, DataVisualizer, StatisticalAnalyzer],
            temperature=0.7
        )
        self.agencii = AgenciiConnector()
        self.active_chat_id = None

    def process_message(self, message, chat_id=None):
        if not self.active_chat_id:
            self.active_chat_id = self.agencii.create_chat()
        return self.agencii.send_message(message, self.active_chat_id)