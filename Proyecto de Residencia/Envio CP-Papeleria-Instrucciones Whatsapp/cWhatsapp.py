import cFileMaker
import requests
import json
import logging

# Configuración de registro de errores
logging.basicConfig(filename='Logs/BitacoraMod1-3.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Configuración de WhatsApp (Asegúrate de configurar la variable de entorno WHATSAPP_ACCESS_TOKEN)
ACCESS_TOKEN = "EAAwlCP39eggBO7oXdza3qfkCotEXTfaZCWuVErBUZBJvLdTEGYLx1FB1OrZAO4gqZBFaB8336Jxem6iZCmUmZCPXUWeBItTtdtzZCBni7XDAHyH4tMMV1H8mZCn2I2zEOgYit18kO3zd68etjtdZAk6Lg1ySAxqb0e9ZBHZARhfcckx4p2M5hKyjoGulJJIfil1ptYOywRdO2tbOzisUuUZC"
PHONE_NUMBER = "528711723602" #8711723602
TEMPLATE_NAME = "carte_porte"

# Función para enviar un mensaje de WhatsApp con un documento adjunto
def send_whatsapp_message(connection, cp_empleado, cp_diario, instrucciones, papeleria):
    try:
        # Extrae variables de CP_PENDEINTES
        id_cp = cp_empleado[0]
        nombre_empleado = cp_empleado[1]
        url_cp = cp_empleado[2] 
        celular_empleado = cp_empleado[3]
        cliente = cp_empleado[4]

        # Extrae variables de CONCEPTO E INSTRUCCIONES
        folio = cp_diario[2]
        concepto = cp_diario[3]

        # Crear el mensaje en formato JSON
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": PHONE_NUMBER,  # Reemplazar por celular_empleado
            "type": "template",
            "template": {
                "name": "carta_porte",
                "language": {
                    "code": "es"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "document",
                                "document": {
                                    # Remplazar por url_cp
                                    "link": "http://cdr.ing.unlp.edu.ar/files/presentaciones/012_Introduccion%20a%20Python.pdf",
                                    "filename": f"{id_cp}.pdf"
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": f"{nombre_empleado}"
                            },
                            {
                                "type": "text",
                                "text": f"{folio}"
                            },
                            {
                                "type": "text",
                                "text": f"{cliente}"
                            },
                            {
                                "type": "text",
                                "text": f"{concepto}"
                            },
                            {
                                "type": "text",
                                "text": f"{papeleria}"
                            },
                            {
                                "type": "text",
                                "text": f"{instrucciones}"
                            }
                        ]
                    }
                ]
            }
        }

        # Realiza la solicitud POST a WhatsApp
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
            # Se hace referencia la metodo Update CP para actualizar el estado de la Carta Porte en la base de datos
            checkUpdate = cFileMaker.update_Estatus_CartaPorte(
                connection,id_cp)
            
            # Se genera el reporte de todos los procesos informativos y erroneos si es el caso.
            if checkUpdate == True:
                logging.info(
                    f"Mensaje enviado correctamente a {nombre_empleado} con número {celular_empleado}")
            else:
                logging.error(
                    f"Error al actualizar filemaker.-> Respuesta del metodo: {checkUpdate}, mensaje de whatsapp exitoso. -> Código de estado: {response.status_code}")
        else:
            logging.error(
                f"Error al enviar el mensaje de whatsapp. Código de estado: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al enviar mensaje de WhatsApp: {e}")
