function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    var toggleButton = document.querySelector(`[onclick="togglePasswordVisibility('${inputId}')"]`);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.innerHTML = `
            <span class="material-symbols-outlined">
                visibility_off
            </span>
        `;
    } else {
        passwordInput.type = "password";
        toggleButton.innerHTML = `
            <span class="material-symbols-outlined">
                visibility
            </span>
        `;
    }
}