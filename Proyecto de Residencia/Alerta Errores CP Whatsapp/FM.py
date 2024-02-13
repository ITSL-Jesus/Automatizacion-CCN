import pyodbc
import logging

# Configurar el registro de registro (registra eventos en un archivo)
logging.basicConfig(filename='Logs/BitacoraMod2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de la cadena de conexión a la base de datos
DB_CONNECTION_STRING = "***************************************************************"

# Función para conectar a la base de datos
def connect_to_database():
    """Conecta a la base de datos y devuelve una conexión o None si no se pudo conectar."""

    try:
        connection = pyodbc.connect(DB_CONNECTION_STRING)
        logging.info("Conexion a la base de datos exitosa.")
        return connection
    except pyodbc.Error as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        return None

# Función para cerrar la conexión de la base de datos de manera segura
def close_database_connection(connection):
    """Cierra la conexión a la base de datos de manera segura."""

    try:
        if connection:
            connection.close()
            logging.info("Conexion a la base de datos cerrada de manera segura.")
    except pyodbc.Error as e:
        logging.error(f"Error al cerrar la conexión a la base de datos: {e}")

# Estatus posibles: Error - Realizado - Pendiente
# Función para buscar los documentos con estatus ERRONEO en las cartas porte
def get_pending_docs(connection):
    """Obtiene los documentos pendientes de timbrar y devuelve una tupla con el folio y el error."""

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                folio_viaje,
                Mensaje_respuesta_timbrado,
                Error_area
            FROM
                carta_porte
            WHERE
                Estatus_xml = 'Error'
                AND
                Bandera_error_whatsapp = 0
            """) 

        row = cursor.fetchall()

        if row is not None:
            return row
        else:
            return None
        
        # #DATA -> Diego 
        #     # tbCartaPorte add campo ErrorArea = [costeo, logistica, RRHH, sistemas]
        #     # DB create new tbAreaError = [ area | encargado | telefono ]
             
        # if area == 'RRHH':
        #     area = 'Recursos Humanos'
            
        # # cursor = connection.cursor()
        # # cursor.execute("""
        # #             SELECT
        # #                 telefono
        # #             FROM
        # #                 ErrorArea
        # #             WHERE
        # #                 area = ?
        # #             """, area)

        # # row = cursor.fetchone()

        # # if row is not None:
        # #         telefono = row[0]
        # #         return folio,error,area,telefono
        # # else:
        # return folio,error,area,telefono
    except pyodbc.Error as e:
        logging.error(f"Error al obtener los errores generados en la carta porte: {e}")
        return None

# Funcion que actualiza el estado del documento en FileMaker a 'Realizado'
def update_status(connection,folio):
    try:
        if folio is not None:
            query = """
                UPDATE carta_porte
                SET Bandera_error_whatsapp = 1
                WHERE folio_viaje = ?
                """
            cursor = connection.cursor()
            cursor.execute(query, (folio))
            connection.commit()
            logging.info(f"Actualizacion exitosa en la carta porte: {folio}")
        else:
            logging.error(f"Error al actualizar el estatus la carta porte {folio}")
    except pyodbc.Error as e:
        logging.error(f"Ocurrio un error en el metodo update_status{e}")
