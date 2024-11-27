from flask import Blueprint, render_template, jsonify
from MetoApi import obtener_clima_por_dia

# Crear el Blueprint
cclima_bp = Blueprint('cclima', __name__, template_folder='templates')

@cclima_bp.route('/')
def clima_home():
    return render_template('meteo.html')

@cclima_bp.route('/weather_data/<departamento>', methods=['GET'])
def weather_data(departamento):
    clima = obtener_clima_por_dia(departamento)
    if 'error' in clima:
        return jsonify(clima), 404
    return jsonify(clima)
