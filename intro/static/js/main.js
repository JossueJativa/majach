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

// Función para abrir la barra lateral
function openSidebar(thisButton) {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.display = "block";
    thisButton.setAttribute("onclick", "closeSidebar(this)");
}

function closeSidebar(thisButton) {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.display = "none";
    thisButton.setAttribute("onclick", "openSidebar(this)");
}

function populateModal(firstName, lastName, username, email, phone, id) {
    document.getElementById('first_name').value = firstName;
    document.getElementById('last_name').value = lastName;
    document.getElementById('username').value = username;
    document.getElementById('email').value = email;
    document.getElementById('phone').value = phone;
    document.getElementById('id').value = id;
}

function populateModalProduct(name, price, stock, id) {
    console.log(name, price, stock, id);
    document.getElementById('name').value = name;
    document.getElementById('price').value = price;
    document.getElementById('stock').value = stock;
    document.getElementById('id_product').value = id;
}