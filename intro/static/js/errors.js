document.getElementById("price").addEventListener('invalid', () => {
    document.getElementById("price").setCustomValidity("El precio debe ser un número mayor a 0");
});

document.getElementById("stock").addEventListener('invalid', () => {
    document.getElementById("stock").setCustomValidity("La cantidad debe ser un número mayor a 0");
});

document.getElementById("phone").addEventListener('invalid', () => {
    document.getElementById("phone").setCustomValidity("El teléfono debe tener 9 a 10 dígitos");
});

document.getElementById("email").addEventListener('invalid', () => {
    document.getElementById("email").setCustomValidity("El correo electrónico no es válido");
});