from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

API_KEY_OPENWEATHER = '0471dcffb143c505ff2ae6507489feb1'

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
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY_OPENWEATHER}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'list' in data and len(data['list']) > 0:
            air_quality_data = data['list'][0]
            pollutants = air_quality_data['components']
            return pollutants
        else:
            print(f"No hay datos de calidad del aire disponibles en la respuesta: {data}")
    except requests.RequestException as e:
        print(f"Error al obtener la calidad del aire: {e}")
    return None