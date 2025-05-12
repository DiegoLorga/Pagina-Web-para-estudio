// Se selecciona el contenedor principal del formulario
const container = document.querySelector('.container');

// Se selecciona el botón que activa el formulario de registro
const registerBtn = document.querySelector('.register-btn');

// Se selecciona el botón que activa el formulario de inicio de sesión
const loginBtn = document.querySelector('.login-btn');

// Al hacer clic en el botón de registro, se añade la clase 'active' al contenedor
// Esto generalmente se usa para mostrar u ocultar el formulario de registro mediante CSS
registerBtn.addEventListener('click', () => {
    container.classList.add('active');
});

// Al hacer clic en el botón de login, se elimina la clase 'active' del contenedor
// Esto vuelve a mostrar el formulario de inicio de sesión
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});
