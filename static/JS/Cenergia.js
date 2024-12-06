document.addEventListener("DOMContentLoaded", () => {
    const mainTitle = document.getElementById("main-title");
    const subtitle = document.getElementById("subtitle");
    const formCard = document.getElementById("form-card");
    const btnSubmit = document.getElementById("btn-submit");

    setTimeout(() => {
        mainTitle.classList.remove("hidden");
        mainTitle.classList.add("visible");
    }, 200);

    setTimeout(() => {
        subtitle.classList.remove("hidden");
        subtitle.classList.add("visible");
    }, 600);

    setTimeout(() => {
        formCard.classList.remove("hidden");
        formCard.classList.add("visible");
    }, 1000);

    setTimeout(() => {
        btnSubmit.classList.remove("hidden");
        btnSubmit.classList.add("visible");
    }, 1400);
});
