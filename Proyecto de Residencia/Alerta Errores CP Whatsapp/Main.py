import FM
import WH
import logging


# Función principal del programa
def main():
    """Inicia el programa y envía mensajes de alerta por WhatsApp para los errores encontrados en las cartas porte."""

    logging.basicConfig(filename='Logs/BitacoraMod2', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Registra un mensaje de inicio en el archivo de registro
    logging.info("Iniciando programa...")

    # Conecta a la base de datos
    connection = FM.connect_to_database()

    # Si la conexión a la base de datos es exitosa
    if connection is not None:
        # Obtiene los datos de los errores pendientes
        infoError = FM.get_pending_docs(connection)
        
        if infoError is not None:

            for error_Data in infoError:
                print(error_Data)
            
                # Si hay errores pendientes en la base de datos
                if error_Data is not None:
                    logging.info("Hay errores pendientes en la base de datos:")
                    logging.info(error_Data)

                    # Envía un mensaje de alerta por WhatsApp
                    WH.send_AlertaError_message(connection, error_Data)
        else:
            logging.info(" -> NO TENEMOS ERRORES PENDIENTES POR RESOLVER <-")

            

    # Si la conexión a la base de datos falla
    else:
        logging.error(
            "No se pudo conectar a la base de datos. Si persiste el problema, llame al ingeniero en turno")
    
    # Cierra la conexión a la base de datos de FileMaker de manera segura
    FM.close_database_connection(connection)
    
    # Registra un mensaje de finalización en el archivo de registro
    logging.info("Programa finalizado. \n")

# Punto de entrada del programa
if __name__ == "__main__":
    # Configura el registro de eventos en un archivo específico
    main()
