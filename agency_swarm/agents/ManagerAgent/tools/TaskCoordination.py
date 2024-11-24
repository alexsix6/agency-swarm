from pydantic import Field
from agency_swarm import BaseTool
from typing import Optional, List

class TaskCoordination(BaseTool):
    """
    Herramienta para la coordinación y asignación de tareas a diferentes agentes.
    """
    task_description: str = Field(
        ...,
        description="Descripción detallada de la tarea a asignar"
    )
    assigned_agent: str = Field(
        ...,
        description="Nombre del agente al que se asignará la tarea (PoliciesAgent, StatisticsAgent, HyvisionAgent, RiskAnalysisAgent)"
    )
    priority: str = Field(
        ...,
        description="Prioridad de la tarea (Alta, Media, Baja)",
    )
    deadline: Optional[str] = Field(
        None,
        description="Fecha límite para completar la tarea (formato: YYYY-MM-DD)"
    )
    dependencies: Optional[List[str]] = Field(
        None,
        description="Lista de tareas que deben completarse antes de esta"
    )

    def run(self):
        # Aquí implementaremos la lógica de asignación de tareas
        response = (
            f"Tarea asignada exitosamente:\n"
            f"- Descripción: {self.task_description}\n"
            f"- Asignada a: {self.assigned_agent}\n"
            f"- Prioridad: {self.priority}\n"
        )
        
        if self.deadline:
            response += f"- Fecha límite: {self.deadline}\n"
        
        if self.dependencies:
            response += f"- Dependencias: {', '.join(self.dependencies)}\n"
            
        return response