# services/twilio_service.py
from twilio.rest import Client
from config.config import app_config

current_config = app_config['development']
client = Client(current_config.TWILIO_ACCOUNT_SID, current_config.TWILIO_AUTH_TOKEN)

# Para pruebas temporales (en services/twilio_service.py)
def enviar_whatsapp(destinatario: str, mensaje: str) -> str:
    try:
        # >>> CAMBIA ESTO SOLO PARA PRUEBAS <<<
        telefono = "+50377523537"  
        
        if not telefono.startswith("+"):
            telefono = f"+503{telefono}"
            
        message = client.messages.create(
            body=mensaje,
            from_=current_config.TWILIO_WHATSAPP_NUMBER,  # Número Twilio
            to=f"whatsapp:{telefono}"  # Tu número verificado
        )
        return "enviado"
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return "fallido"