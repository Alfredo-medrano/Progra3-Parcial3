import requests

API_KEY = 'CfLoPjnKHuRGYIp8'
BASE_URL = 'https://my.meteoblue.com/packages/basic-day'

departamentos = {
    'San Salvador': {'lat': 13.692, 'lon': -89.2182},
    'Santa Ana': {'lat': 13.9946, 'lon': -89.5597},
    'San Miguel': {'lat': 13.4833, 'lon': -88.1833},
    'La Libertad': {'lat': 13.4904, 'lon': -89.2906},
    'Ahuachapán': {'lat': 13.9212, 'lon': -89.845},
    'Sonsonate': {'lat': 13.7184, 'lon': -89.7117},
    'Usulután': {'lat': 13.335, 'lon': -88.4419},
    'La Paz': {'lat': 13.524, 'lon': -88.9434},
    'Cabañas': {'lat': 13.850, 'lon': -88.8833},
    'Chalatenango': {'lat': 14.0333, 'lon': -88.9333},
    'Morazán': {'lat': 13.6667, 'lon': -88.1167},
    'San Vicente': {'lat': 13.6333, 'lon': -88.8},
    'Cuscatlán': {'lat': 13.7178, 'lon': -88.9019},
    'La Unión': {'lat': 13.3333, 'lon': -87.8333}
}

def obtener_clima_por_dia(departamento):
    if departamento not in departamentos:
        return {'error': f'Departamento "{departamento}" no encontrado'}
    
    lat = departamentos[departamento]['lat']
    lon = departamentos[departamento]['lon']
    url = f'{BASE_URL}?lat={lat}&lon={lon}&apikey={API_KEY}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        data_day = data.get("data_day", {})
        if not data_day:
            return {'error': 'Datos no disponibles en la API para este departamento'}
        
        days = len(data_day.get("time", []))
        temperature_max = data_day.get("temperature_max", [])
        temperature_min = data_day.get("temperature_min", [])
        
        forecast = []
        for i in range(days):
            forecast.append({
                "date": data_day["time"][i] if i < len(data_day["time"]) else "No disponible",
                "temp_max": temperature_max[i] if i < len(temperature_max) else "No disponible",
                "temp_min": temperature_min[i] if i < len(temperature_min) else "No disponible"
            })
        
        return forecast

    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {'error': 'Error al obtener datos del clima'}
    except KeyError as e:
        print(f"Error al procesar la respuesta de la API: {e}")
        return {'error': 'Datos incompletos o malformados recibidos'}