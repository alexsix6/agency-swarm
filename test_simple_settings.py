import json

def generate_simplified_settings():
    settings = {
        "agency_name": "Enterprise_Management_Agency",
        "version": "1.0.0",
        "description": "Sistema multiagente para gestion empresarial",
        "agents": [
            {
                "name": "ManagerAgent",
                "description": "Central coordinator and decision maker",
                "instructions": "Coordinates and manages all agency activities",
                "tools": [
                    {
                        "name": "TaskCoordination",
                        "description": "Coordina tareas",
                        "parameters": {
                            "task_description": {
                                "type": "string",
                                "description": "Descripcion de tarea",
                                "required": True
                            },
                            "assigned_agent": {
                                "type": "string",
                                "description": "Agente asignado",
                                "required": True
                            },
                            "priority": {
                                "type": "string",
                                "description": "Prioridad",
                                "required": True
                            }
                        }
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
        ],
        "communication_flows": [
            ["ManagerAgent", "PoliciesAgent"]
        ],
        "api_configurations": {
            "openai": {
                "api_key_env": "OPENAI_API_KEY"
            }
        }
    }

    # Guardar sin caracteres especiales y con formato simple
    with open('settings_simple.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=True)
        print("✓ Archivo settings_simple.json generado")

if __name__ == "__main__":
    generate_simplified_settings()