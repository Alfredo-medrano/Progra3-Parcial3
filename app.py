from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from login import login_bp  

app = Flask(__name__)
app.secret_key = '123456'  
app.register_blueprint(login_bp)  


API_KEY_METEOSOURCE = 'nce9e73tukc0zenzl52hcd2xnojbc8c45e595gfi'

cities = [
    'San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 'Usulután',
    'Sonsonate', 'La Unión', 'Ahuachapán', 'Cuscatlán', 'Chalatenango',
    'Cabañas', 'San Vicente', 'Morazán'
]

city_coordinates = {
    'San Salvador': {'lat': 13.6929, 'lon': -89.2182},
    'Santa Ana': {'lat': 13.9946, 'lon': -89.5597},
    'San Miguel': {'lat': 13.4833, 'lon': -88.1833},
    'La Libertad': {'lat': 13.4883, 'lon': -89.3222},
    'Usulután': {'lat': 13.3500, 'lon': -88.4333},
    'Sonsonate': {'lat': 13.7167, 'lon': -89.7267},
    'La Unión': {'lat': 13.3369, 'lon': -87.8439},
    'Ahuachapán': {'lat': 13.9214, 'lon': -89.8450},
    'Cuscatlán': {'lat': 13.7333, 'lon': -88.9333},
    'Chalatenango': {'lat': 14.0333, 'lon': -88.9333},
    'Cabañas': {'lat': 13.9167, 'lon': -88.6333},
    'San Vicente': {'lat': 13.6333, 'lon': -88.8000},
    'Morazán': {'lat': 13.7667, 'lon': -88.1000}
}

def get_coordinates(city):
    return city_coordinates.get(city, None)

def get_air_quality(lat, lon):
    url = f'https://www.meteosource.com/api/v1/free/point?lat={lat}&lon={lon}&sections=air_quality&language=es&units=metric&key={API_KEY_METEOSOURCE}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'current' in data and 'air_quality' in data['current']:
            air_quality = data['current']['air_quality']
            return air_quality
        else:
            print(f"No hay datos de calidad del aire disponibles en la respuesta: {data}")
    except requests.RequestException as e:
        print(f"Error al obtener la calidad del aire: {e}")
    return None

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
    graphJSON = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graphJSON

@app.route('/')
def home():
    if 'user_logged_in' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_logged_in' not in session:
        return redirect(url_for('login.login'))
    
    data = None
    graphJSON = None
    if request.method == 'POST':
        selected_city = request.form['city']
        coords = get_coordinates(selected_city)
        if coords:
            air_quality = get_air_quality(coords['lat'], coords['lon'])
            if air_quality and 'pollutants' in air_quality:
                pollutants = air_quality['pollutants']
                data = pd.DataFrame([
                    {'Contaminante': key, 'Concentración': value['concentration']}
                    for key, value in pollutants.items()
                ])
                graphJSON = plot_graph(data)
            else:
                data = pd.DataFrame()
        else:
            data = pd.DataFrame()
    return render_template('index.html', data=data, graphJSON=graphJSON, cities=cities)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    city = request.form['city']
    coords = get_coordinates(city)
    if coords:
        air_quality = get_air_quality(coords['lat'], coords['lon'])
        if air_quality and 'pollutants' in air_quality:
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Informe de Calidad del Aire para {city}")
            p.drawString(100, 730, "Contaminantes y Concentraciones:")
            y_position = 710
            pollutants = air_quality['pollutants']
            for pollutant, info in pollutants.items():
                concentration = info['concentration']
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

if __name__ == '__main__':
    app.run(debug=True)
