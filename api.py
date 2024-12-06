import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

API_KEY_OPENWEATHER = '0471dcffb143c505ff2ae6507489feb1'

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

contaminantes_nombres = {
    "pm10": "Partículas PM10",
    "pm2_5": "Partículas PM2.5",
    "no2": "Dióxido de Nitrógeno",
    "so2": "Dióxido de Azufre",
    "o3": "Ozono",
    "co": "Monóxido de Carbono"
}

def get_coordinates(city):
    if city in city_coordinates:
        return city_coordinates[city]
    else:
        print(f"Ciudad '{city}' no encontrada.")
        return None

def get_air_quality(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY_OPENWEATHER}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'list' in data and len(data['list']) > 0:
            air_quality_data = data['list'][0]['components']
            return air_quality_data
        else:
            print(f"No hay datos de calidad del aire disponibles en la respuesta: {data}")
    except requests.RequestException as e:
        print(f"Error al obtener la calidad del aire: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    
    return None

def generate_pdf(air_quality_data, city_name):
    file_name = f'Calidad_Aire_{city_name}.pdf'
    c = canvas.Canvas(file_name, pagesize=letter)
    
    c.drawString(100, 750, f"Reporte de Calidad del Aire para {city_name}")
    c.drawString(100, 730, "Contaminantes y sus concentraciones:")
    
    y_position = 710
    for contaminante, concentracion in air_quality_data.items():
        contaminante_nombre = contaminantes_nombres.get(contaminante, contaminante)
        c.drawString(100, y_position, f"{contaminante_nombre}: {concentracion} μg/m³")
        y_position -= 20
    
    c.save()
    print(f"Reporte generado: {file_name}")

if __name__ == "__main__":
    # Ejemplo de uso
    ciudad = "San Salvador"
    coords = get_coordinates(ciudad)
    if coords:
        air_quality = get_air_quality(coords['lat'], coords['lon'])
        if air_quality:
            generate_pdf(air_quality, ciudad)
        else:
            print("No se pudo obtener la calidad del aire.")
    else:
        print("No se pudieron obtener las coordenadas de la ciudad.")
