document.addEventListener("DOMContentLoaded", () => {
    const togglePin = document.getElementById("togglePin");
    const pinInput = document.getElementById("pin");

    togglePin.addEventListener("click", () => {
        if (pinInput.type === "password") {
            pinInput.type = "text";
            togglePin.textContent = "🙈";
        } else {
            pinInput.type = "password";
            togglePin.textContent = "👁️";
        }
    });
});