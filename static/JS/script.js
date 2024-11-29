document.addEventListener('DOMContentLoaded', function () {
    const departamentoSelect = document.getElementById('departamento');
    const forecastContainer = document.getElementById('forecast');
    const loadingSpinner = document.getElementById('loading');

    function mostrarSpinner() {
        loadingSpinner.classList.remove('hidden');
        forecastContainer.innerHTML = '';
    }

    function ocultarSpinner() {
        loadingSpinner.classList.add('hidden');
    }

    function mostrarPronostico(data) {
        console.log("Datos recibidos del servidor:", data);
        forecastContainer.innerHTML = ''; 
        if (data.error) {
            forecastContainer.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        data.forEach(day => {
            const dayCard = `
                <div class="card">
                    <h3>${day.date}</h3>
                    <p>Max: ${day.temp_max}°C</p>
                    <p>Min: ${day.temp_min}°C</p>
                </div>
            `;
            forecastContainer.innerHTML += dayCard;
        });
    }

    departamentoSelect.addEventListener('change', function () {
        const departamento = departamentoSelect.value;

        mostrarSpinner();

        fetch(`/cclima/weather_data/${departamento}`)
            .then(response => response.json())
            .then(data => {
                ocultarSpinner();
                mostrarPronostico(data);
            })
            .catch(error => {
                console.error("Error al obtener datos:", error); // Depuración
                ocultarSpinner();
                forecastContainer.innerHTML = '<p>Error al obtener los datos</p>';
            });
    });

    departamentoSelect.dispatchEvent(new Event('change'));
});
