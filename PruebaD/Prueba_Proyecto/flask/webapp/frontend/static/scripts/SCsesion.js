document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const responseMessage = document.getElementById('response-message');

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario: username, password: password })
        });

        const data = await response.json();
        
        // Verificar el estado de la respuesta
        if (response.status === 200) {
            // Login exitoso
            responseMessage.style.color = "green";
            responseMessage.textContent = data.message || "Login exitoso"; // Si no hay mensaje, muestra un mensaje por defecto.

            setTimeout(()=>{
                window.location.href = "/menu_cita";
            },1500);

        } else if (response.status === 400) {
            // Error de validación de datos
            responseMessage.style.color = "red";
            responseMessage.textContent = data.message || "Usuario y contraseña son requeridos";
        } else if (response.status === 401) {
            // Usuario o contraseña incorrectos
            responseMessage.style.color = "red";
            responseMessage.textContent = data.message || "Usuario o contraseña incorrectos";
        } else if (response.status === 500) {
            // Error del servidor
            responseMessage.style.color = "red";
            responseMessage.textContent = "Error en el servidor. Por favor, inténtalo nuevamente.";
        } else {
            // Otros errores no previstos
            responseMessage.style.color = "red";
            responseMessage.textContent = "Error desconocido.";
        }
    } catch (error) {
        // Error de conexión o problema con la solicitud
        responseMessage.style.color = "red";
        responseMessage.textContent = "Error en la conexión. Verifica tu conexión a internet o inténtalo más tarde.";
    }
});

