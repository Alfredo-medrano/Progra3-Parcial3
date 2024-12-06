document.addEventListener("DOMContentLoaded", () => {
    const departamentos = {
        'San Salvador': { lat: 13.692, lon: -89.2182 },
        'Santa Ana': { lat: 13.9946, lon: -89.5597 },
        'San Miguel': { lat: 13.4833, lon: -88.1833 },
        'La Libertad': { lat: 13.4904, lon: -89.2906 },
        'Ahuachapán': { lat: 13.9212, lon: -89.845 },
        'Sonsonate': { lat: 13.7184, lon: -89.7117 },
        'Usulután': { lat: 13.335, lon: -88.4419 },
        'La Paz': { lat: 13.524, lon: -88.9434 },
        'Cabañas': { lat: 13.85, lon: -88.8833 },
        'Chalatenango': { lat: 14.0333, lon: -88.9333 },
        'Morazán': { lat: 13.6667, lon: -88.1167 },
        'San Vicente': { lat: 13.6333, lon: -88.8 },
        'Cuscatlán': { lat: 13.7178, lon: -88.9019 },
        'La Unión': { lat: 13.3333, lon: -87.8333 }
    };

    const selectElement = document.getElementById('departamento');
    Object.keys(departamentos).forEach(dep => {
        const option = document.createElement('option');
        option.value = dep;
        option.textContent = dep;
        selectElement.appendChild(option);
    });

    window.getWeatherData = async () => {
        const departamento = selectElement.value;
        const { lat, lon } = departamentos[departamento];
        const url = `https://my.meteoblue.com/packages/basic-day?lat=${lat}&lon=${lon}&apikey=CfLoPjnKHuRGYIp8`;

        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('forecast').innerHTML = '';

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('No se pudieron obtener los datos del clima');
            const data = await response.json();

            document.getElementById('loading').classList.add('hidden');

            const forecastContainer = document.getElementById('forecast');
            const days = data.data_day?.time || [];
            const tempMax = data.data_day?.temperature_max || [];
            const tempMin = data.data_day?.temperature_min || [];

            days.forEach((day, index) => {
                const card = document.createElement('div');
                card.classList.add('card');
                card.innerHTML = `
                    <h4>${day}</h4>
                    <i class="wi ${index % 2 === 0 ? 'wi-day-sunny' : 'wi-night-alt-cloudy'}"></i>
                    <p>Máx: ${tempMax[index] || 'N/A'}°C</p>
                    <p>Mín: ${tempMin[index] || 'N/A'}°C</p>
                `;
                forecastContainer.appendChild(card);
            });
        } catch (error) {
            document.getElementById('loading').classList.add('hidden');
            alert(error.message);
        }
    };
});
