# Importamos las clases que vamos a utilizar
import cFileMaker
import cWhatsapp
import logging

# Programa para enviar mensajes de alerta por WhatsApp para los errores encontrados en las carta porte
def main():
    # Configurar el registro de registro
    logging.basicConfig(filename='Logs/BitacoraMod1-3.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Iniciando programa...")

    # Co3necta a la base de datos
    connection = cFileMaker.connect_to_database()

    # n guarda el numero de cartas porte pendientes al momento de ejecutar el programa, mediante el metodo get_count
    n = cFileMaker.get_count(connection)
    logging.info(f"Tenemos: {n} CARTAS PORTE pendientes en la base de datos:")

    # Si la conexión es exitosa
    if connection is not None:
        # Obtiene los datos de los errores pendientes

        # -> CP_Empleados guarda los datos retornados por el metodo get_pending_docs como:
        # id_cartaPorte, Nombre del operador, la ruta de la CP, el telefono empresarial de
        #  la empleado y el cliente
        cp_empleados = cFileMaker.get_pending_docs(connection)
            
        # Si hay CARTAS PORTE pendientes procedemos a enviar el mensaje por whatsapp
        if cp_empleados is not None:
            
            # -> CP_Diario guarda los datos retornados por el metodo get_concept_and_client_operatio
            #  como: id_concepto, id_cliente, folio y la descricpicon del concepto
            for cp_Data in cp_empleados:
                print(cp_Data)
                cp_diario = cFileMaker.get_concept_and_client_operation(connection, cp_Data)

                # -> Intrucciones guarda una serie de pasos estipulados para cliente y tipo de opereacion los cuales son retornados por el metodo get_instructions
                intrucciones = cFileMaker.get_instructions(connection, cp_diario)

                # -> Papeleria guarda una lista de los documentos requeridos por el cliente, las cuales son retornados por el metodo get_stationery
                papeleria = cFileMaker.get_stationery(connection, cp_diario)
            
                # Envía un mensaje informativo por WhatsApp el cual contiene la carta porte, el folio, el cliente, el empleado,las intrucciones y la papeleria requerida
                cWhatsapp.send_whatsapp_message(connection, cp_Data, cp_diario, intrucciones, papeleria)
            
                # Cremos el registro de los datos que vamos a utilizar el se guardaran en el archivo RegistroModulo1.log
                logging.info(cp_Data)
                logging.info(f"La informacion a tratar es: {cp_diario}")
                
        else:
            logging.info("NO TENEMOS CARTAS PORTE PENDINTES POR ENVIAR")

    # Si la conexión a la base de datos falla
    else:
        logging.error(
            "No se pudo conectar a la base de datos. Si persiste el problema llame al ingeniero en turno")

    # Cierra la conexión a la base de datos
    #connection.close()
    logging.info("Programa finalizado. \n")


if __name__ == "__main__":
    main()
