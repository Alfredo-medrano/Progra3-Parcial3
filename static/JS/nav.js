document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");

    menuToggle.addEventListener("click", () => {
        menu.classList.toggle("show");
    });

    document.addEventListener("click", (event) => {
        if (!menu.contains(event.target) && event.target !== menuToggle) {
            menu.classList.remove("show");
        }
    });
});
