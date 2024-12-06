document.addEventListener("DOMContentLoaded", () => {
    const citySelect = document.getElementById("city");
    const selectedCityInput = document.getElementById("selected-city");

    citySelect.addEventListener("change", () => {
        const selectedCity = citySelect.value;
        selectedCityInput.value = selectedCity;
    });
});
