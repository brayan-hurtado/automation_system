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

class Automatized_MG:
    def __init__(self):
        self.usuarios = []
        self.solicitudes = []