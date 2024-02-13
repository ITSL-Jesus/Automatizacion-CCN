# Importa las bibliotecas necesarias
import pyodbc
import logging

# Configura la generación de registros de errores en un archivo de registro
logging.basicConfig(filename='Logs/BitacoraMod1-3.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura la cadena de conexión a la base de datos (debes configurar la variable de entorno DB_CONNECTION_STRING)
DB_CONNECTION_STRING = "********************************************************"

# Función para conectar a la base de datos
def connect_to_database():
    try:
        connection = pyodbc.connect(DB_CONNECTION_STRING)
        logging.info("Conexion a la base de datos exitosa.")
        return connection
    except pyodbc.Error as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        return None

# Función para cerrar la conexión de la base de datos de manera segura
def close_database_connection(connection):
    try:
        if connection:
            connection.close()
            logging.info("Conexion a la base de datos cerrada.")
    except pyodbc.Error as e:
        logging.error(f"Error al cerrar la conexión a la base de datos: {e}")

# Función para obtener documentos pendientes y sus detalles
def get_pending_docs(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                c.id_carta_porte,
                c.oper_Nombre_operador,
                c.Path_pdf,
                e.Telefono_celular_empresa,
                c.Cliente_operacion
            FROM
                carta_porte c 
                INNER JOIN
                empleado e
                ON
                c.oper_Id_operador = e.id_empleado
            WHERE
                c.Estatus_timbrado = 'Pendiente'
            AND
                c.Estatus_xml = 'Realizado'
            AND
                c.Estatus_pdf = 'Realizado'
            AND 
                c.Estatus_whatsapp != 'Realizado'
        """)

         
        # Recupera todas las fila de resultados
        row = cursor.fetchall()
        if row is not None:
            return row
        else:
            return None

    except pyodbc.Error as e:
        logging.error(
            f"Error al obtener datos de los documentos pendientes: {e}")
        return None

# Función para obtener conceptos y cliente de una carta porte
def get_concept_and_client_operation(connection, data):
    id = data[0]
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                d.CLAVE_CONCEPTO,
                d.Id_cliente_operacion,
                d.FOLIO,
                d.CONCEPTO
            FROM
                diario as d 
                INNER JOIN
                carta_porte as c
                ON
                d.FOLIO = c.folio_viaje
            WHERE
                c.id_carta_porte = ?
        """, id)

        # Recupera la primera fila de resultados
        row = cursor.fetchone()

        # Desglozamos row para un mayor entendimiento.
        if row is not None:
            id_concepto = row[0]
            id_cliente_op = row[1]
            folio = row[2]
            concepto = row[3]
            return id_concepto, id_cliente_op, folio, concepto
        else:
            return None

    except pyodbc.Error as e:
        logging.error(
            f"Error al obtener datos del cliente y concepto correspondiente a la papelería e instrucciones: {e}")
        return None

# Función para obtener instrucciones relacionadas con un concepto
def get_instructions(connection, data):
    concepto = data[0]
    id = data[1]
    try:
        cursor = connection.cursor()
        cursor.execute("""
              SELECT
               Nombre_instrucciones_concepto
            FROM
               Instrucciones_concepto
            WHERE
               Id_concepto = ?
               AND 
               Id_cliente_operacion = ?
        """, concepto, id)

        # Recupera todas las filas de resultados
        rows = cursor.fetchall()
        instrucciones = ''

        # Validamos rows para evitar retornar una cadena vacia.
        if rows == []:
            instrucciones = 'No hay instrucciones para este concepto'
            return instrucciones

        else:
            instrucciones = str(rows)

            # Mediante el for damos formato la cadena de texto para solo dejar las palabras.
            for simbolo in ['(', ')', ',,', '[', ']']:
                instrucciones = instrucciones.replace(simbolo, '')

            instrucciones = instrucciones[:-2]
            instrucciones = instrucciones[1:]
            instrucciones = instrucciones.replace("' '", " -")

            return instrucciones

    except pyodbc.Error as e:
        logging.error(
            f"Error al obtener las instrucciones correspondientes a la carta porte: {e}")
        return None

# Función para obtener información de la papelería asociada a un cliente de operación
def get_stationery(connection, data):
    id = data[1]
    try:
        cursor = connection.cursor()
        cursor.execute("""
              SELECT
               Nombre_papeleria
            FROM
               Papeleria_cliente_operacion
            WHERE
               Id_cliente_operacion = ?
        """, id)

        # Recupera todas las filas de resultados
        rows = cursor.fetchall()
        papeleria = ''

        # Validamos rows para evitar retornar una cadena vacia.
        if rows == []:
            papeleria = 'No hay papeleria asignada para este concepto'
            return papeleria

        else:
            papeleria = str(rows)

            # Mediante el for damos formato la cadena de texto para solo dejar las palabras.
            for simbolo in ['(', ')', ',,', '[', ']']:
                papeleria = papeleria.replace(simbolo, '')

            papeleria = papeleria[:-2]
            papeleria = papeleria[1:]
            papeleria = papeleria.replace("' '", " -")

            return papeleria

    except pyodbc.Error as e:
        logging.error(
            f"Error al obtener la papelería correspondiente a la carta porte: {e}")
        return None

# Función para obtener el número de documentos con estatus de pendiente
def get_count(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            id_carta_porte
        FROM
            carta_porte
        WHERE
            Estatus_timbrado = 'Pendiente'
            AND
            Estatus_xml = 'Realizado'
            AND
            Estatus_pdf = 'Realizado'
            AND
            Estatus_whatsapp != 'Realizado'
    """)
    row = cursor.fetchall()
    n = len(row)
    return n

# Función para actualiza el estado de Estatus_timbrado y Estatus_whatsapp en la base de datos
def update_Estatus_CartaPorte(connection, id_cp):
    try:
        Estatus_timbrado_whapp = "Timbrado con exito por whatsapp"
        Estatus_whatsapp = "Realizado"
        query = """
            UPDATE carta_porte
            SET 
            Estatus_timbrado_whapp = ?, Estatus_whatsapp = ?
            WHERE
              id_carta_porte = ?
            """
        cursor = connection.cursor()
        cursor.execute(query, (Estatus_timbrado_whapp, Estatus_whatsapp, id_cp))
        connection.commit()
        return True
    except Exception as e:
        logging.error(f"Error durante la actualización: {str(e)}")
        return False
