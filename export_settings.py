import json
import os
import textwrap

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

def convert_parameters_to_input_schema(parameters):
    input_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    for param_name, param_info in parameters.items():
        # Añadir 'description' si no existe
        param_description = param_info.get("description", "")
        input_schema['properties'][param_name] = {
            "type": param_info["type"],
            "description": param_description
        }
        if param_info.get("required", False):
            input_schema["required"].append(param_name)
    # Eliminar 'required' si está vacío
    if not input_schema["required"]:
        del input_schema["required"]
    return input_schema

def generate_settings():
    """Genera un archivo settings.json con la configuración de la agencia"""
    
    # Configuración de la agencia
    settings = {
        "agency_name": "Enterprise Management Agency",
        "version": "1.0.0",
        "description": "Sistema multiagente para gestion empresarial automatizada",
        "agents": []
    }

    # Lista de agentes con las correcciones aplicadas
    agents = [
        {
            "name": "ManagerAgent",
            "description": "Central coordinator and decision maker for the agency",
            "instructions": """
                # Manager Agent Instructions
                Coordinates and manages all agency activities, including task assignment,
                progress monitoring, and decision making.
            """,
            "tools": [
                {
                    "name": "TaskCoordination",
                    "description": "Coordina y asigna tareas a diferentes agentes",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "task_description": {"type": "string", "required": True, "description": "Descripción de la tarea"},
                        "assigned_agent": {"type": "string", "required": True, "description": "Agente asignado"},
                        "priority": {"type": "string", "required": True, "description": "Prioridad de la tarea"},
                        "deadline": {"type": "string", "required": False, "description": "Fecha límite"}
                    })
                },
                {
                    "name": "ProgressMonitor",
                    "description": "Monitorea el progreso de tareas y proyectos",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "project_id": {"type": "string", "required": True, "description": "ID del proyecto"},
                        "action": {"type": "string", "required": True, "description": "Acción a realizar"},
                        "progress_update": {"type": "integer", "required": False, "description": "Actualización de progreso"}
                    })
                },
                {
                    "name": "DecisionSupport",
                    "description": "Apoya la toma de decisiones",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "decision_type": {"type": "string", "required": True, "description": "Tipo de decisión"},
                        "context": {"type": "string", "required": True, "description": "Contexto de la decisión"},
                        "options": {"type": "array", "required": True, "description": "Opciones disponibles"}
                    })
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        },
        # Repite el mismo proceso para los demás agentes...
        {
            "name": "PoliciesAgent",
            "description": "Corporate policy and regulation expert",
            "instructions": """
                # Policies Agent Instructions
                Manages and interprets corporate policies, ensuring compliance and 
                providing guidance on regulatory matters.
            """,
            "tools": [
                {
                    "name": "DocumentSearch",
                    "description": "Busca documentos de políticas",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "search_query": {"type": "string", "required": True, "description": "Consulta de búsqueda"},
                        "document_type": {"type": "string", "required": True, "description": "Tipo de documento"}
                    })
                },
                {
                    "name": "ComplianceChecker",
                    "description": "Verifica cumplimiento de políticas",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "activity_description": {"type": "string", "required": True, "description": "Descripción de la actividad"},
                        "applicable_policies": {"type": "array", "required": True, "description": "Políticas aplicables"}
                    })
                }
            ],
            "temperature": 0.6,
            "max_tokens": 4000
        },
        # Continúa con StatisticsAgent, HyvisionAgent y RiskAnalysisAgent aplicando las mismas correcciones...
        {
            "name": "StatisticsAgent",
            "description": "Data analysis and insights generator",
            "instructions": """
                # Statistics Agent Instructions
                Analyzes data using BigQuery, generates insights, and provides 
                statistical support to other agents.
            """,
            "tools": [
                {
                    "name": "BigQueryConnector",
                    "description": "Conecta y ejecuta consultas en BigQuery",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "query": {"type": "string", "required": True, "description": "Consulta a ejecutar"},
                        "dataset": {"type": "string", "required": True, "description": "Conjunto de datos"}
                    })
                },
                {
                    "name": "DataVisualizer",
                    "description": "Genera visualizaciones de datos",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "data_source": {"type": "string", "required": True, "description": "Fuente de datos"},
                        "visualization_type": {"type": "string", "required": True, "description": "Tipo de visualización"}
                    })
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        },
        {
            "name": "HyvisionAgent",
            "description": "Hyvision software technical specialist",
            "instructions": """
                # Hyvision Agent Instructions
                Provides technical support and documentation for the Hyvision system.
            """,
            "tools": [
                {
                    "name": "TechnicalDocManager",
                    "description": "Gestiona documentación técnica",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "doc_type": {"type": "string", "required": True, "description": "Tipo de documento"},
                        "content": {"type": "string", "required": False, "description": "Contenido del documento"}
                    })
                },
                {
                    "name": "SystemDiagnostics",
                    "description": "Realiza diagnósticos del sistema",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "diagnostic_type": {"type": "string", "required": True, "description": "Tipo de diagnóstico"},
                        "system_component": {"type": "string", "required": True, "description": "Componente del sistema"}
                    })
                }
            ],
            "temperature": 0.6,
            "max_tokens": 4000
        },
        {
            "name": "RiskAnalysisAgent",
            "description": "Physical risk assessment specialist",
            "instructions": """
                # Risk Analysis Agent Instructions
                Evaluates physical risks, generates safety recommendations, and 
                coordinates risk mitigation strategies.
            """,
            "tools": [
                {
                    "name": "RiskEvaluator",
                    "description": "Evalúa riesgos físicos",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "area": {"type": "string", "required": True, "description": "Área a evaluar"},
                        "risk_category": {"type": "string", "required": True, "description": "Categoría de riesgo"}
                    })
                },
                {
                    "name": "MitigationPlanner",
                    "description": "Planifica estrategias de mitigación",
                    "type": "function",
                    "input_schema": convert_parameters_to_input_schema({
                        "risk_id": {"type": "string", "required": True, "description": "ID del riesgo"},
                        "risk_level": {"type": "string", "required": True, "description": "Nivel de riesgo"}
                    })
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
    ]

    # Aplicar limpieza y ajuste a los agentes
    for agent in agents:
        agent['name'] = clean_string(agent['name'])
        agent['description'] = clean_string(agent['description'])
        agent['instructions'] = clean_string(textwrap.dedent(agent['instructions']))
        # Limpiar herramientas
        for tool in agent['tools']:
            tool['name'] = clean_string(tool['name'])
            tool['description'] = clean_string(tool['description'])
            tool['type'] = clean_string(tool['type'])
            # Limpiar 'input_schema'
            properties = tool['input_schema']['properties']
            for param_name, param_info in properties.items():
                param_info['type'] = clean_string(param_info['type'])
                param_info['description'] = clean_string(param_info['description'])
            if 'required' in tool['input_schema']:
                tool['input_schema']['required'] = [clean_string(r) for r in tool['input_schema']['required']]
    
    settings['agents'] = agents

    # Añadir flujos de comunicación y configuraciones de API
    settings['communication_flows'] = [
        ["ManagerAgent", "PoliciesAgent"],
        ["ManagerAgent", "StatisticsAgent"],
        ["ManagerAgent", "HyvisionAgent"],
        ["ManagerAgent", "RiskAnalysisAgent"],
        ["StatisticsAgent", "RiskAnalysisAgent"]
    ]
    settings['api_configurations'] = {
        "openai": {
            "api_key_env": "OPENAI_API_KEY"
        }
    }

    # Guardar en archivo
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
            print("✓ Archivo settings.json generado exitosamente")
            print(f"✓ Ubicación: {os.path.abspath('settings.json')}")
            print("\n✓ Todo listo para importar en Agencii.ai")
        return True
    except Exception as e:
        print(f"\n❌ Error al guardar el archivo: {str(e)}")
        return False

if __name__ == "__main__":
    generate_settings()