from pydantic import Field
from agency_swarm import BaseTool
from typing import Optional

class ProgressMonitor(BaseTool):
    """
    Herramienta para monitorear el progreso de tareas y proyectos.
    """
    project_id: str = Field(
        ...,
        description="Identificador del proyecto o tarea a monitorear"
    )
    action: str = Field(
        ...,
        description="Acción a realizar (check_status, update_progress, generate_report)"
    )
    progress_update: Optional[int] = Field(
        None,
        description="Porcentaje de progreso (0-100) para actualizaciones",
        ge=0,
        le=100
    )
    status_notes: Optional[str] = Field(
        None,
        description="Notas adicionales sobre el estado o progreso"
    )

    def run(self):
        # Aquí implementaremos la lógica de monitoreo
        if self.action == "check_status":
            return f"Estado actual del proyecto {self.project_id}: En progreso"
        elif self.action == "update_progress":
            return f"Progreso actualizado al {self.progress_update}% para el proyecto {self.project_id}"
        elif self.action == "generate_report":
            return (
                f"Reporte generado para el proyecto {self.project_id}:\n"
                f"- Progreso actual: {self.progress_update}%\n"
                f"- Notas: {self.status_notes}"
            )