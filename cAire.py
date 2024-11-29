from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from api import *
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

cAire_bp = Blueprint('cAire', __name__)

contaminantes_nombres = {
    "pm10": "Partículas PM10",
    "pm2_5": "Partículas PM2.5",
    "no2": "Dióxido de Nitrógeno",
    "so2": "Dióxido de Azufre",
    "o3": "Ozono",
    "co": "Monóxido de Carbono"
}

def plot_graph(data):
    plt.figure(figsize=(10, 5))
    plt.bar(data['Contaminante'], data['Concentración'], color='blue')
    plt.xlabel('Contaminante')
    plt.ylabel('Concentración (μg/m³)')
    plt.title('Calidad del Aire')
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graphJSON = base64.b64encode(img.getvalue()).decode('utf-8')  # Codificamos en base64 y decodificamos a utf-8
    plt.close()
    return graphJSON


@cAire_bp.route('/aire', methods=['GET', 'POST'])
def aire():
    if 'user_logged_in' not in session:
        return redirect(url_for('login.login'))
    
    data = None
    graphJSON = None
    cities = [
    'Ahuachapán', 'Cabañas', 'Chalatenango', 'La Libertad', 
    'La Paz', 'La Unión', 'Morazán', 'San Miguel', 'San Salvador', 
    'San Vicente', 'Santa Ana', 'Sonsonate', 'Usulután', 'Cuscatlán'
]

    if request.method == 'POST':
        selected_city = request.form['city']
        coords = get_coordinates(selected_city)
        if coords:
            air_quality = get_air_quality(coords['lat'], coords['lon'])
            if air_quality:
                data = pd.DataFrame([{
                    'Contaminante': key, 'Concentración': value
                } for key, value in air_quality.items()])
                graphJSON = plot_graph(data)  # Generar la gráfica
            else:
                data = pd.DataFrame()
        else:
            data = pd.DataFrame()
    return render_template(
        'cAire.html', 
        data=data, 
        graphJSON=graphJSON,  # Pasar la gráfica a la plantilla
        cities=cities, 
        contaminantes_nombres=contaminantes_nombres
    )

@cAire_bp.route('/generate_report', methods=['POST'])
def generate_report():
    city = request.form['city']
    coords = get_coordinates(city)
    if coords:
        air_quality = get_air_quality(coords['lat'], coords['lon'])
        if air_quality:
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Informe de Calidad del Aire para {city}")
            p.drawString(100, 730, "Contaminantes y Concentraciones:")
            y_position = 710
            for pollutant, concentration in air_quality.items():
                p.drawString(100, y_position, f"{pollutant}: {concentration} μg/m³")
                y_position -= 20
            p.save()
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'informe_calidad_aire_{city}.pdf',
                mimetype='application/pdf'
            )
    return "No se pudo generar el informe."
