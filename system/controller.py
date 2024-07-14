from bd_connector import *

class Usuario_sesion:
    def __init__(self, idUser, userName, password, worker_role, estado):
        self.__idUser = idUser
        self.__userName = userName
        self.__password = password
        self.worker_role = worker_role
        self.estado = estado

class Asesor_SAC:
    def __init__(self,idWorker, userName, password, worker_role, estado, nombre, apellido, localidad, telefono):
        super().__init__(userName, password, worker_role, estado)
        self.__idWorker = idWorker
        self.nombre = nombre
        self.apellido = apellido
        self.localidad = localidad
        self.telefono = telefono
        self.solicitudes = Solicitudes() #Relación de composición.

class BackOffice:
    def __init__(self, idBO, userName, password, estado, nombre, apellido, localidad, worker_role, telefono):
        super().__init__(userName, password, estado)
        self.__idBO = idBO
        self.nombre = nombre
        self.apellido = apellido
        self.localidad = localidad
        self.worker_role = worker_role
        self.telefono = telefono

class Solicitudes:
    def __init__(self, servicio, logica, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign, IdOrden=None, status='Abierta'):
        self.IdOrden = IdOrden
        self.servicio = servicio
        self.logica = logica
        self.status = status
        self.clientName = clientName
        self.clientPlace = clientPlace
        self.clientTel = clientTel
        self.rut = rut
        self.descripcion = descripcion
        self.deadline = deadline
        self.dateAsign = dateAsign
        self.dateUpdated = None
    
    @staticmethod
    def mostrar_datos(IdOrden):
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
           sql = "SELECT IdOrden, servicio, logica, status, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign, dateUpdated FROM solicitudes WHERE IdOrden = %s"
           cursor.execute(sql, (IdOrden,))
           consulta = cursor.fetchone()
        conexion.close()
        return consulta
    
    @staticmethod
    def listar_datos():
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT IdOrden, servicio, logica, status, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign, dateUpdated FROM solicitudes"
            cursor.execute(sql)
            busqueda = cursor.fetchall()
            total = len(busqueda)
        conexion.close()
        return busqueda
    
    @classmethod
    def crear_solicitud(cls, solicitud):
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "INSERT INTO solicitudes(servicio, logica, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (solicitud.servicio, solicitud.logica, solicitud.clientName, solicitud.clientPlace, solicitud.clientTel, solicitud.rut, solicitud.descripcion, solicitud.deadline, solicitud.dateAsign))
            solicitud.IdOrden = cursor.lastrowid
            conexion.commit()
            new_rows = cursor.rowcount
        return new_rows
    
    @staticmethod
    def obtener_orden_id(IdOrden):
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT IdOrden, servicio, logica, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign FROM solicitudes WHERE IdOrden=%s"
            cursor.execute(sql, (IdOrden,))
            solicitud = cursor.fetchone()
        conexion.close()
        return solicitud
    
    @classmethod
    def update_request(cls, solicitud):
        try:
            conexion = obtener_conexion()
            if not conexion:
                print("No se pudo establecer la conexión con la base de datos.")
                return

            # Verificar si el IdOrden existe antes de intentar actualizar
            if not cls.exists_id_orden(solicitud.IdOrden):
                print(f"El IdOrden {solicitud.IdOrden} no existe en la base de datos.")
                return

            with conexion.cursor() as cursor:
                sql = """
                    UPDATE solicitudes 
                    SET servicio=%s, logica=%s, clientName=%s, clientPlace=%s, clientTel=%s, rut=%s, 
                        descripcion=%s, deadline=%s, dateAsign=%s 
                    WHERE IdOrden=%s
                """
                values = (
                    solicitud.servicio, solicitud.logica, solicitud.clientName, solicitud.clientPlace, 
                    solicitud.clientTel, solicitud.rut, solicitud.descripcion, 
                    solicitud.deadline, solicitud.dateAsign, solicitud.IdOrden
                )
                print("Consulta SQL:", sql)
                print("Valores:", values)
            
                cursor.execute(sql, values)
                conexion.commit()
            
            # Verifica cuántas filas fueron afectadas
            if cursor.rowcount == 0:
                print("No se actualizó ninguna fila. Verifica que el IdOrden sea correcto.")
            else:
                print(f"Filas actualizadas: {cursor.rowcount}")

        except pymysql.MySQLError as e:
            print(f"Ocurrió un error en la base de datos: {e}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            if conexion:
                conexion.close()
                
    @classmethod
    def exists_id_orden(cls, IdOrden):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM solicitudes WHERE IdOrden = %s"
                cursor.execute(sql, (IdOrden,))
                result = cursor.fetchone()
                return result[0] > 0 if result else False
        except pymysql.MySQLError as e:
            print(f"Ocurrió un error en la base de datos: {e}")
            return False
        finally:
            if conexion:
                conexion.close()

class Automatized_MG:
    def __init__(self):
        self.usuarios = []
        self.solicitudes = []