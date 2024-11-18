document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const responseMessage = document.getElementById('response-message');

    try {
        const response = await fetch('/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario: username, password: password })
        });

        const data = await response.json();
        
        // Verificar el estado de la respuesta
        if (response.status === 201) {
            // Registro exitoso
            responseMessage.style.color = "green";
            responseMessage.textContent = data.message || "Usuario creado exitosamente . Redirigiendo a Inicio";

            setTimeout(()=>{
                window.location.href = "/";
            },1500);

        } else if (response.status === 400) {
            // Error de validación de datos
            responseMessage.style.color = "red";
            responseMessage.textContent = data.message || "Usuario y contraseña son requeridos";
        } else if (response.status === 409) {
            // Usuario ya existe
            responseMessage.style.color = "red";
            responseMessage.textContent = data.message || "El usuario ya existe";
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
