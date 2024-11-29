    document.addEventListener("DOMContentLoaded", function() {
    const resultBox = document.querySelector(".result-box");
    const header = document.querySelector(".header h1");

    setTimeout(function() {
        header.style.opacity = "1";
        header.style.transition = "opacity 1s ease-in-out";
    }, 300);

    setTimeout(function() {
        resultBox.style.opacity = "1";
        resultBox.style.transform = "translateY(0)";
        resultBox.style.transition = "opacity 0.8s ease-out, transform 0.8s ease-out";
    }, 600);
    setTimeout(function() {
        resultBox.style.opacity = "1";
        resultBox.style.transform = "translateX(0)";
        resultBox.style.transition = "opacity 1s ease-out, transform 1s ease-out";
    }, 1000);
});
