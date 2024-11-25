import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

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
        self.active_chats = {}  # Para mantener registro de chats activos

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

    def create_chat(self):
        """Crea una nueva sesión de chat"""
        try:
            payload = {
                "apiIntegrationId": self.api_integration_id
            }
            response = requests.post(
                f"{self.base_url}/create_new_chat/",
                headers=self.headers,
                json=payload
            )
            if response.status_code == 200:
                chat_id = response.json().get('chatId')
                self.active_chats[chat_id] = {
                    'created_at': datetime.now(),
                    'messages': []
                }
                print(f"Chat creado exitosamente. ID: {chat_id}")
                return chat_id
            else:
                print(f"Error creando chat: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creando chat: {str(e)}")
            return None

    def send_message(self, message, chat_id=None):
        """Envía un mensaje y recibe respuesta"""
        try:
            if not chat_id:
                chat_id = self.create_chat()
                if not chat_id:
                    return None

            payload = {
                "message": message,
                "apiIntegrationId": self.api_integration_id,
                "chatId": chat_id,
                "attachments": []
            }

            response = requests.post(
                f"{self.base_url}/get_completion/",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                response_data = response.json()
                # Guardar mensaje en el historial
                if chat_id in self.active_chats:
                    self.active_chats[chat_id]['messages'].append({
                        'message': message,
                        'response': response_data,
                        'timestamp': datetime.now()
                    })
                return response_data
            else:
                print(f"Error enviando mensaje: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error enviando mensaje: {str(e)}")
            return None

    def get_chat_history(self, chat_id):
        """Obtiene el historial de un chat específico"""
        return self.active_chats.get(chat_id, {}).get('messages', [])

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

def run_test_conversation():
    """Función para probar una conversación completa"""
    connector = AgenciiConnector()
    
    print("\n=== Iniciando prueba de conversación ===")
    
    # Probar conexión
    if not connector.test_connection():
        print("❌ Error en la conexión inicial")
        return

    # Crear nuevo chat
    chat_id = connector.create_chat()
    if not chat_id:
        print("❌ Error creando chat")
        return

    # Probar una conversación
    test_messages = [
        "Necesito un análisis de riesgos para el área de producción",
        "¿Puedes mostrarme las estadísticas de incidentes del último mes?",
        "¿Cuáles son las políticas de seguridad aplicables?"
    ]

    for message in test_messages:
        print(f"\nEnviando mensaje: {message}")
        response = connector.send_message(message, chat_id)
        if response:
            print(f"Respuesta recibida: {response.get('message', {}).get('content', 'No content')}")
        else:
            print("❌ Error recibiendo respuesta")

    # Mostrar historial
    print("\n=== Historial de la conversación ===")
    history = connector.get_chat_history(chat_id)
    for idx, interaction in enumerate(history, 1):
        print(f"\nInteracción {idx}:")
        print(f"Usuario: {interaction['message']}")
        print(f"Asistente: {interaction['response'].get('message', {}).get('content', 'No content')}")

if __name__ == "__main__":
    print("Iniciando integración con Agencii...")
    
    # Verificar/Crear archivo .env
    if not os.path.exists('.env'):
        print("\nNo se encontró archivo .env")
        api_key = input("Por favor, introduce tu API Key de Agencii: ")
        with open('.env', 'w') as f:
            f.write(f"AGENCII_API_KEY={api_key}")
        print("✓ Archivo .env creado exitosamente")
    
    # Ejecutar prueba de conversación
    run_test_conversation()