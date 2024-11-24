from agency_swarm.agents import Agent

class TestAgent(Agent):
    def __init__(self):
        super().__init__(name="TestAgent",
                         description="This is a test agent",
                         instructions="Your instructions here.")

    def get_completion(self, message):
        # Método que procesa el mensaje y devuelve una respuesta.
        return f"I received your message: {message}"