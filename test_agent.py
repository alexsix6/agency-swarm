from agency_swarm.agents.TestAgent.TestAgent import TestAgent

# Inicializa el agente
agent = TestAgent()

# Verifica si el método get_completion existe antes de usarlo
if hasattr(agent, 'get_completion') and callable(getattr(agent, 'get_completion')):
    # Prueba con un mensaje simple
    response = agent.get_completion("Hello, TestAgent! How can you help me today?")
    print("Response from TestAgent:", response)
else:
    print("Error: The 'TestAgent' class does not have a 'get_completion' method. Please implement it.")