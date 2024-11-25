import json
import os
from datetime import datetime

def ensure_settings_dir():
    """Asegura que existe el directorio settings y devuelve su ruta"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    settings_dir = os.path.join(current_dir, 'settings')
    
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
        print(f"✓ Carpeta settings creada en: {settings_dir}")
    
    return settings_dir

def validate_agent_schema(agent_name, schema):
    """Valida que el schema del agente tenga todos los componentes necesarios"""
    required_components = {
        "name": "string",
        "description": "string",
        "collaborators": "array",
        "tools": "array"
    }
    
    properties = schema["components"]["schemas"][agent_name]["properties"]
    validation_results = {
        "is_valid": True,
        "missing_components": [],
        "invalid_types": []
    }
    
    for component, expected_type in required_components.items():
        if component not in properties:
            validation_results["is_valid"] = False
            validation_results["missing_components"].append(component)
        elif properties[component]["type"] != expected_type:
            validation_results["is_valid"] = False
            validation_results["invalid_types"].append(
                f"{component}: expected {expected_type}, got {properties[component]['type']}"
            )
    
    return validation_results

def verify_existing_instructions(agent_name):
    """Verifica que existan las instrucciones en la carpeta del agente"""
    instructions_path = os.path.join("agency_swarm", "agents", agent_name, "instructions.md")
    exists = os.path.exists(instructions_path)
    if not exists:
        print(f"⚠️ Advertencia: No se encuentra instructions.md para {agent_name}")
    return exists

def generate_complete_settings():
    settings = {
        "openapi": "3.1.0",
        "info": {
            "title": "Enterprise Management Agency",
            "version": "1.0.0"
        },
        "components": {
            "schemas": {
                "ManagerAgent": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string", "default": "Central coordinator and decision maker"},
                        "collaborators": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["PoliciesAgent", "StatisticsAgent", "HyvisionAgent", "RiskAnalysisAgent"]
                            }
                        },
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "task_description": {
                                                "type": "string",
                                                "description": "Task details"
                                            },
                                            "assigned_agent": {
                                                "type": "string",
                                                "description": "Agent to assign"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "PoliciesAgent": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string", "default": "Policy and compliance specialist"},
                        "collaborators": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["ManagerAgent"]
                            }
                        },
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "policy_query": {
                                                "type": "string",
                                                "description": "Policy search query"
                                            },
                                            "document_type": {
                                                "type": "string",
                                                "description": "Type of policy document"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "StatisticsAgent": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string", "default": "Data analysis specialist"},
                        "collaborators": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["ManagerAgent", "RiskAnalysisAgent"]
                            }
                        },
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "query": {
                                                "type": "string",
                                                "description": "BigQuery query"
                                            },
                                            "dataset": {
                                                "type": "string",
                                                "description": "Dataset name"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "HyvisionAgent": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string", "default": "Technical system specialist"},
                        "collaborators": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["ManagerAgent"]
                            }
                        },
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "system_component": {
                                                "type": "string",
                                                "description": "Component to analyze"
                                            },
                                            "action_type": {
                                                "type": "string",
                                                "description": "Type of technical action"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "RiskAnalysisAgent": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string", "default": "Risk assessment specialist"},
                        "collaborators": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["ManagerAgent", "StatisticsAgent"]
                            }
                        },
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "area": {
                                                "type": "string",
                                                "description": "Area to evaluate"
                                            },
                                            "risk_category": {
                                                "type": "string",
                                                "description": "Risk category"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "communication_flows": {
            "type": "object",
            "properties": {
                "synchronous": {"type": "boolean", "default": True},
                "flows": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "default": [
                        ["ManagerAgent", "PoliciesAgent"],
                        ["ManagerAgent", "StatisticsAgent"],
                        ["ManagerAgent", "HyvisionAgent"],
                        ["ManagerAgent", "RiskAnalysisAgent"],
                        ["StatisticsAgent", "RiskAnalysisAgent"]
                    ]
                }
            }
        }
    }

    try:
        # Obtener directorio settings
        settings_dir = ensure_settings_dir()
        
        # Timestamp para verificación
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nGenerando archivos de configuración - {timestamp}")
        
        # Guardar para cada agente por separado
        agents = ["ManagerAgent", "PoliciesAgent", "StatisticsAgent", "HyvisionAgent", "RiskAnalysisAgent"]
        
        for agent in agents:
            # Verificar existencia de instrucciones
            verify_existing_instructions(agent)
            
            # Validar schema
            validation_results = validate_agent_schema(agent, settings)
            if not validation_results["is_valid"]:
                print(f"\n⚠️ Advertencia en schema de {agent}:")
                if validation_results["missing_components"]:
                    print("  Componentes faltantes:", ", ".join(validation_results["missing_components"]))
                if validation_results["invalid_types"]:
                    print("  Tipos inválidos:")
                    for error in validation_results["invalid_types"]:
                        print(f"    - {error}")
                print("  Continuando con la generación...\n")
            
            # Generar settings del agente
            agent_settings = {
                "openapi": "3.1.0",
                "info": {
                    "title": f"{agent} Specification",
                    "version": "1.0.0",
                    "generated_at": timestamp
                },
                "components": {
                    "schemas": {
                        agent: settings["components"]["schemas"][agent]
                    }
                },
                "communication": {
                    "synchronous": True,
                    "collaborators": settings["components"]["schemas"][agent]["properties"]["collaborators"]["items"]["enum"]
                }
            }
            
            # Crear archivo en la carpeta settings
            filepath = os.path.join(settings_dir, f"{agent.lower()}_settings.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(agent_settings, f, indent=2)
            print(f"✓ Archivo {agent.lower()}_settings.json generado exitosamente")
            print(f"  Ubicación: {filepath}")
        
        # Guardar configuración completa
        complete_settings_path = os.path.join(settings_dir, 'complete_settings.json')
        with open(complete_settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        print(f"\n✓ Archivo complete_settings.json generado exitosamente")
        print(f"  Ubicación: {complete_settings_path}")
        
        print("\n✓ Todos los archivos generados correctamente")
        print(f"  Carpeta: {settings_dir}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"  Ubicación del error: {os.path.abspath('.')}")

if __name__ == "__main__":
    generate_complete_settings()