from flask import Flask, render_template, redirect, request, url_for, flash
from system.controller import *

app = Flask(__name__)
app.secret_key = "super secret key"

msg = ''
tipo = ''

@app.route("/")
@app.route('/Data_base', methods=['GET', 'POST'])
def home():
    solicitudes = Solicitudes.listar_datos()
    return render_template('Data_base.html', solicitudes = solicitudes)

@app.route('/asesor_sac')
def asesor():
    solicitudes = Solicitudes.listar_datos()
    return render_template('asesor_sac.html', solicitudes = solicitudes)

@app.route('/registro_solicitud', methods=['GET', 'POST'])
def formulario_registro_solicitud():
    return render_template('registro_solicitud.html')

@app.route('/guardar_solicitud', methods=['POST'])
def guardar_solicitud():
    if request.method == 'POST':
        servicio = request.form['servicio']
        logica = request.form['logica']
        clientName = request.form['clientName']
        clientPlace = request.form['clientPlace']
        clientTel = request.form['clientTel']
        rut = request.form['rut']
        descripcion = request.form['descripcion']
        deadline = request.form['deadline']
        dateAsign = request.form['dateAsign']
        
        solicitud = Solicitudes(servicio, logica, clientName, clientPlace, clientTel, rut, descripcion, deadline, dateAsign)
        Solicitudes.crear_solicitud(solicitud)    
    return redirect(url_for('home'))

@app.route("/ver_detalles_solicitud/<int:IdOrden>", methods=['GET'])
def viewDetalles(IdOrden):
    if request.method == 'GET':
        solicitud = Solicitudes.mostrar_datos(IdOrden)
        if solicitud:
            return render_template('view.html', infoSolicitud = solicitud, msg='Detalles de la solicitud', tipo=1)
        else:
            return render_template('Data_base.html', msg = 'No existe la solicitud', tipo=1)
    return redirect(url_for('home'))