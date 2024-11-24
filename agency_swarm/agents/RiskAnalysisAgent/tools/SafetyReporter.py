from pydantic import Field
from agency_swarm import BaseTool
from typing import Optional, List, Dict

class SafetyReporter(BaseTool):
    """
    Herramienta para generar reportes de seguridad y seguimiento de medidas.
    """
    report_type: str = Field(
        ...,
        description="Tipo de reporte (incident, audit, compliance, improvement)"
    )
    time_period: str = Field(
        ...,
        description="Período del reporte"
    )
    metrics: List[str] = Field(
        ...,
        description="Métricas de seguridad a incluir"
    )
    incidents: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Lista de incidentes a reportar"
    )
    recommendations: Optional[List[str]] = Field(
        None,
        description="Recomendaciones de mejora"
    )

    def run(self):
        # Implementar lógica de generación de reportes
        response = (
            f"Generando reporte de seguridad:\n"
            f"Tipo: {self.report_type}\n"
            f"Período: {self.time_period}\n"
            f"Métricas incluidas:\n"
        )
        
        for metric in self.metrics:
            response += f"- {metric}\n"
            
        if self.incidents:
            response += "\nIncidentes reportados:\n"
            for incident in self.incidents:
                for key, value in incident.items():
                    response += f"- {key}: {value}\n"
                    
        if self.recommendations:
            response += "\nRecomendaciones:\n"
            for rec in self.recommendations:
                response += f"- {rec}\n"
                
        return response + "\nReporte generado (simulado)"