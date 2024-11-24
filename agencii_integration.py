import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AgenciiConnector:
    def __init__(self):
        self.base_url = "https://agency-swarm-app-japboyzddq-uc.a.run.app"
        self.api_integration_id = "5jYQQ9KQAg80Qd9b9qln"  # ID proporcionado
        self.headers = {
            'Authorization': f'Bearer {os.getenv("AGENCII_API_KEY")}',
            'Content-Type': 'application/json'
        }

    def test_connection(self):
        """Prueba la conexión con Agencii"""
        payload = {
            "message": "Test connection",
            "apiIntegrationId": self.api_integration_id,
            "attachments": []
        }
        try:
            print("Enviando solicitud de prueba...")
            response = requests.post(
                f"{self.base_url}/get_completion/",
                headers=self.headers,
                json=payload
            )
            print(f"Código de estado: {response.status_code}")
            return response.json()
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None

    def format_agents_for_agencii(self):
        """Formatea los agentes para Agencii"""
        try:
            # Leer el archivo settings.json existente
            with open('settings.json', 'r', encoding='utf-8') as f:
                current_settings = json.load(f)

            # Formatear para Agencii
            agencii_format = {
                "name": "Enterprise_Management_Agency",
                "apiIntegrationId": self.api_integration_id,
                "agents": []
            }

            # Convertir cada agente al formato de Agencii
            for agent in current_settings["agents"]:
                agencii_agent = {
                    "name": agent["name"],
                    "role": agent["description"],
                    "tools": []
                }
                
                # Convertir herramientas al formato de Agencii
                for tool in agent["tools"]:
                    agencii_tool = {
                        "name": tool["name"],
                        "type": "function",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                param_name: {
                                    "type": param_info["type"],
                                    "description": param_info.get("description", ""),
                                    "required": param_info.get("required", False)
                                }
                                for param_name, param_info in tool["parameters"].items()
                            }
                        }
                    }
                    agencii_agent["tools"].append(agencii_tool)
                
                agencii_format["agents"].append(agencii_agent)

            # Guardar el nuevo formato
            with open('agencii_settings.json', 'w', encoding='utf-8') as f:
                json.dump(agencii_format, f, indent=2)
            
            print("✓ Archivo agencii_settings.json generado exitosamente")
            return agencii_format

        except Exception as e:
            print(f"Error formateando agentes: {str(e)}")
            return None

    def import_agents(self):
        """Importa los agentes a Agencii"""
        try:
            # Obtener el formato de agentes
            agencii_format = self.format_agents_for_agencii()
            if not agencii_format:
                return "Error en el formateo de agentes"

            # Preparar payload
            payload = {
                "message": "Import agents",
                "apiIntegrationId": self.api_integration_id,
                "settings": agencii_format,
                "attachments": []
            }

            # Enviar solicitud
            print("Enviando solicitud de importación...")
            response = requests.post(
                f"{self.base_url}/get_completion/",
                headers=self.headers,
                json=payload
            )
            print(f"Código de estado: {response.status_code}")
            return response.json()

        except Exception as e:
            print(f"Error importando agentes: {str(e)}")
            return None

if __name__ == "__main__":
    print("Iniciando integración con Agencii...")
    
    # Verificar/Crear archivo .env
    if not os.path.exists('.env'):
        print("\nNo se encontró archivo .env")
        api_key = input("Por favor, introduce tu API Key de Agencii: ")
        with open('.env', 'w') as f:
            f.write(f"AGENCII_API_KEY={api_key}")
        print("✓ Archivo .env creado exitosamente")
    
    # Inicializar el conector
    connector = AgenciiConnector()
    
    # Probar conexión
    print("\nProbando conexión con Agencii...")
    connection_result = connector.test_connection()
    if connection_result:
        print("✓ Conexión exitosa")
        
        # Importar agentes
        print("\nIniciando importación de agentes...")
        import_result = connector.import_agents()
        print(f"Resultado de importación: {import_result}")
    else:
        print("✗ Error en la conexión")