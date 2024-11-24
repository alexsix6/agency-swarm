from pydantic import Field
from agency_swarm import BaseTool
from typing import List, Optional

class DecisionSupport(BaseTool):
    """
    Herramienta para apoyar la toma de decisiones basada en inputs de otros agentes.
    """
    decision_type: str = Field(
        ...,
        description="Tipo de decisión (resource_allocation, risk_assessment, priority_setting)"
    )
    context: str = Field(
        ...,
        description="Contexto detallado de la situación que requiere decisión"
    )
    options: List[str] = Field(
        ...,
        description="Lista de opciones disponibles para la decisión"
    )
    criteria: Optional[List[str]] = Field(
        None,
        description="Criterios a considerar para la decisión"
    )
    agent_inputs: Optional[dict] = Field(
        None,
        description="Diccionario con inputs de otros agentes relevantes para la decisión"
    )

    def run(self):
        # Aquí implementaremos la lógica de soporte a decisiones
        response = (
            f"Análisis de decisión para {self.decision_type}:\n"
            f"Contexto: {self.context}\n"
            f"Opciones disponibles:\n"
        )
        
        for i, option in enumerate(self.options, 1):
            response += f"{i}. {option}\n"
            
        if self.criteria:
            response += "\nCriterios considerados:\n"
            for criterion in self.criteria:
                response += f"- {criterion}\n"
                
        if self.agent_inputs:
            response += "\nInputs de otros agentes:\n"
            for agent, input_ in self.agent_inputs.items():
                response += f"- {agent}: {input_}\n"
                
        return response