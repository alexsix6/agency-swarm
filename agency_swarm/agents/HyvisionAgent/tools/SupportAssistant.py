from pydantic import Field
from agency_swarm import BaseTool
from typing import Optional, List

class SupportAssistant(BaseTool):
    """
    Herramienta para asistencia y soporte técnico de Hyvision.
    """
    issue_type: str = Field(
        ...,
        description="Tipo de problema (technical, configuration, performance, user_error)"
    )
    description: str = Field(
        ...,
        description="Descripción detallada del problema"
    )
    priority: str = Field(
        ...,
        description="Prioridad del problema (high, medium, low)"
    )
    affected_modules: Optional[List[str]] = Field(
        None,
        description="Módulos del sistema afectados"
    )
    previous_actions: Optional[List[str]] = Field(
        None,
        description="Acciones ya intentadas para resolver el problema"
    )

    def run(self):
        # Implementar lógica de asistencia técnica
        response = (
            f"Procesando solicitud de soporte:\n"
            f"Tipo de problema: {self.issue_type}\n"
            f"Descripción: {self.description}\n"
            f"Prioridad: {self.priority}\n"
        )
        
        if self.affected_modules:
            response += "Módulos afectados:\n"
            for module in self.affected_modules:
                response += f"- {module}\n"
                
        if self.previous_actions:
            response += "Acciones previas:\n"
            for action in self.previous_actions:
                response += f"- {action}\n"
                
        return response + "\nSolución propuesta (simulada)"