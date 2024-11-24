import json
import os

def clean_string(text):
    """Limpia strings de caracteres especiales y formatos"""
    # Reemplazar caracteres especiales comunes
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '#': '', '\n': ' ', '  ': ' '
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

def generate_settings():
    """Genera un archivo settings.json con la configuración de la agencia"""
    
    # Configuración simplificada de la agencia
    settings = {
        "agency_name": "Enterprise Management Agency",
        "version": "1.0.0",
        "description": "Sistema multiagente para gestión empresarial automatizada",
        "agents": [
            {
                "name": "ManagerAgent",
                "description": "Central coordinator and decision maker for the agency",
                "instructions": """# Manager Agent Instructions
                Coordinates and manages all agency activities, including task assignment,
                progress monitoring, and decision making.""",
                "tools": [
                    {
                        "name": "TaskCoordination",
                        "description": "Coordina y asigna tareas a diferentes agentes",
                        "parameters": {
                            "task_description": {"type": "string", "required": True},
                            "assigned_agent": {"type": "string", "required": True},
                            "priority": {"type": "string", "required": True},
                            "deadline": {"type": "string", "required": False}
                        }
                    },
                    {
                        "name": "ProgressMonitor",
                        "description": "Monitorea el progreso de tareas y proyectos",
                        "parameters": {
                            "project_id": {"type": "string", "required": True},
                            "action": {"type": "string", "required": True},
                            "progress_update": {"type": "integer", "required": False}
                        }
                    },
                    {
                        "name": "DecisionSupport",
                        "description": "Apoya la toma de decisiones",
                        "parameters": {
                            "decision_type": {"type": "string", "required": True},
                            "context": {"type": "string", "required": True},
                            "options": {"type": "array", "required": True}
                        }
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            {
                "name": "PoliciesAgent",
                "description": "Corporate policy and regulation expert",
                "instructions": """# Policies Agent Instructions
                Manages and interprets corporate policies, ensuring compliance and 
                providing guidance on regulatory matters.""",
                "tools": [
                    {
                        "name": "DocumentSearch",
                        "description": "Busca documentos de políticas",
                        "parameters": {
                            "search_query": {"type": "string", "required": True},
                            "document_type": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "ComplianceChecker",
                        "description": "Verifica cumplimiento de políticas",
                        "parameters": {
                            "activity_description": {"type": "string", "required": True},
                            "applicable_policies": {"type": "array", "required": True}
                        }
                    }
                ],
                "temperature": 0.6,
                "max_tokens": 4000
            },
            {
                "name": "StatisticsAgent",
                "description": "Data analysis and insights generator",
                "instructions": """# Statistics Agent Instructions
                Analyzes data using BigQuery, generates insights, and provides 
                statistical support to other agents.""",
                "tools": [
                    {
                        "name": "BigQueryConnector",
                        "description": "Conecta y ejecuta consultas en BigQuery",
                        "parameters": {
                            "query": {"type": "string", "required": True},
                            "dataset": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "DataVisualizer",
                        "description": "Genera visualizaciones de datos",
                        "parameters": {
                            "data_source": {"type": "string", "required": True},
                            "visualization_type": {"type": "string", "required": True}
                        }
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            {
                "name": "HyvisionAgent",
                "description": "Hyvision software technical specialist",
                "instructions": """# Hyvision Agent Instructions
                Provides technical support and documentation for the Hyvision system.""",
                "tools": [
                    {
                        "name": "TechnicalDocManager",
                        "description": "Gestiona documentación técnica",
                        "parameters": {
                            "doc_type": {"type": "string", "required": True},
                            "content": {"type": "string", "required": False}
                        }
                    },
                    {
                        "name": "SystemDiagnostics",
                        "description": "Realiza diagnósticos del sistema",
                        "parameters": {
                            "diagnostic_type": {"type": "string", "required": True},
                            "system_component": {"type": "string", "required": True}
                        }
                    }
                ],
                "temperature": 0.6,
                "max_tokens": 4000
            },
            {
                "name": "RiskAnalysisAgent",
                "description": "Physical risk assessment specialist",
                "instructions": """# Risk Analysis Agent Instructions
                Evaluates physical risks, generates safety recommendations, and 
                coordinates risk mitigation strategies.""",
                "tools": [
                    {
                        "name": "RiskEvaluator",
                        "description": "Evalúa riesgos físicos",
                        "parameters": {
                            "area": {"type": "string", "required": True},
                            "risk_category": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "MitigationPlanner",
                        "description": "Planifica estrategias de mitigación",
                        "parameters": {
                            "risk_id": {"type": "string", "required": True},
                            "risk_level": {"type": "string", "required": True}
                        }
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
        ],
        "communication_flows": [
            ["ManagerAgent", "PoliciesAgent"],
            ["ManagerAgent", "StatisticsAgent"],
            ["ManagerAgent", "HyvisionAgent"],
            ["ManagerAgent", "RiskAnalysisAgent"],
            ["StatisticsAgent", "RiskAnalysisAgent"]
        ],
        "api_configurations": {
            "openai": {
                "api_key_env": "OPENAI_API_KEY"
            }
        }
    }

    # Guardar en archivo
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
            print("✓ Archivo settings.json generado exitosamente")
            print(f"✓ Ubicación: {os.path.abspath('settings.json')}")
            print("\n✓ Todo listo para importar en Agencii.ai")
    except Exception as e:
        print(f"\n❌ Error al guardar el archivo: {str(e)}")

if __name__ == "__main__":
    generate_settings()