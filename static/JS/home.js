document.addEventListener("DOMContentLoaded", () => {
    const exploreButton = document.getElementById("exploreButton");

    exploreButton.addEventListener("click", (event) => {
        alert("Redirigiendo a la página de pronósticos...");
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(".animate");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    });

    elements.forEach(element => observer.observe(element));
});
