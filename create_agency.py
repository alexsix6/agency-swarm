from typing import List, Any
from agency_swarm import Agency
from agency_swarm.agents.ManagerAgent.ManagerAgent import ManagerAgent
from agency_swarm.agents.PoliciesAgent.PoliciesAgent import PoliciesAgent
from agency_swarm.agents.StatisticsAgent.StatisticsAgent import StatisticsAgent
from agency_swarm.agents.HyvisionAgent.HyvisionAgent import HyvisionAgent
from agency_swarm.agents.RiskAnalysisAgent.RiskAnalysisAgent import RiskAnalysisAgent
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv('OPENAI_API_KEY'):
    raise EnvironmentError("OPENAI_API_KEY no encontrada en las variables de entorno")

# Instanciar agentes
manager = ManagerAgent()
policies = PoliciesAgent()
statistics = StatisticsAgent()
hyvision = HyvisionAgent()
risk_analysis = RiskAnalysisAgent()

# Crear la estructura de agencia con tipos explícitos
agency_structure: List[Any] = [
    manager,  # Punto de entrada principal
    [manager, policies],  # Manager puede comunicarse con Policies
    [manager, statistics],  # Manager puede comunicarse con Statistics
    [manager, hyvision],  # Manager puede comunicarse con Hyvision
    [manager, risk_analysis],  # Manager puede comunicarse con Risk Analysis
    [statistics, risk_analysis],  # Statistics puede comunicarse con Risk Analysis
]

# Crear la agencia con la estructura de comunicación
agency = Agency(
    agency_structure,
    shared_instructions='agency_specs.md',
    temperature=0.7,
    max_prompt_tokens=4000,
    type='messages'  # Añadimos este parámetro para resolver el warning de Gradio
)

if __name__ == "__main__":
    print("Iniciando Enterprise Management Agency...")
    print("Agentes disponibles:", [agent.name for agent in [manager, policies, statistics, hyvision, risk_analysis]])
    
    # Opción 1: Configurar el chatbot con parámetros específicos
    import gradio as gr
    
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(type="messages")
        agency.demo_gradio(chatbot=chatbot)