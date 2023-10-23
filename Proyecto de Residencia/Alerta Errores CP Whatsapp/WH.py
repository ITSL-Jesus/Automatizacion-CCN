import requests
import FM
import logging

# Configurar el registro de registro (registra eventos en un archivo)
logging.basicConfig(filename='Logs/BitacoraMod2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Establece el token de acceso, el número de teléfono del destinatario y el nombre de la plantilla
ACCESS_TOKEN = "EAAwlCP39eggBO7oXdza3qfkCotEXTfaZCWuVErBUZBJvLdTEGYLx1FB1OrZAO4gqZBFaB8336Jxem6iZCmUmZCPXUWeBItTtdtzZCBni7XDAHyH4tMMV1H8mZCn2I2zEOgYit18kO3zd68etjtdZAk6Lg1ySAxqb0e9ZBHZARhfcckx4p2M5hKyjoGulJJIfil1ptYOywRdO2tbOzisUuUZC"
TEMPLATE_NAME = "errores"

def send_AlertaError_message(connection, infoerror):
    """Envía un mensaje de alerta de error de WhatsApp al número de teléfono especificado.

    Args:
        connection: Una conexión a la base de datos de FileMaker.
        infoerror: Una tupla que contiene el folio y el mensaje de error, etc...
    """

    try:
        #Extraemos las variables de la tupla InfoError
        folio = infoerror[0]
        error = infoerror[1]
        area = infoerror[2]
        telefono = "528711723602"

        # Crea el contenido de la solicitud POST
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{telefono}", #Cambiar por numero de telefono del encargado...
            "type": "template",
            "template": {
                "name": TEMPLATE_NAME,
                "language": {
                    "code": "es"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "link": "https://img-qn.51miz.com/Element/01/00/69/56/23e1efeb_E1006956_f1995deb.jpg"
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": f"{area}"
                            },
                            {
                                "type": "text",
                                "text": f"{folio}"
                            },
                            {
                                "type": "text",
                                "text": f"{error}"
                            }
                        ]
                    }
                ]
            }
        }

        # Realiza la solicitud POST a la API de WhatsApp de Facebook
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"https://graph.facebook.com/v17.0/116295554906490/messages",
            headers=headers,
            json=payload
        )

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            logging.info(
                f"Mensaje enviado correctamente al numero {telefono}")
            FM.update_status(connection,folio)

        else:
            # Registra un error si la solicitud no se completó con éxito
            logging.error(
                f"Error al enviar el mensaje. Código de estado: {response.status_code}")


    except requests.exceptions.RequestException as e:
        # Registra un error si se produce una excepción al enviar el mensaje de WhatsApp
        logging.error(f"Error en la funcion send_AlertaError_message: {e}")

