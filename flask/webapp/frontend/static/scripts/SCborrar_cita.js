document.getElementById('delete-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    // Obtener el ID de la cita desde el formulario
    const citaId = document.getElementById('cita-id').value.trim();
    const responseMessage = document.getElementById('response-message');

    // Validar que el campo no esté vacío
    if (!citaId) {
        responseMessage.style.color = "red";
        responseMessage.textContent = "Por favor, proporciona el número de cita.";
        return;
    }

    try {
        // Realizar la solicitud DELETE al servidor
        const response = await fetch('/borrar_cita', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ numeroDeCita: citaId }) // Enviar el número de cita en el cuerpo
        });

        // Procesar la respuesta del servidor
        const data = await response.json();

        if (response.ok) {
            // Eliminación exitosa
            responseMessage.style.color = "green";
            responseMessage.textContent = data.message || "Cita eliminada exitosamente.";

            setTimeout(()=>{
                window.location.href = "/menu_cita";
            },1000);

        } else {
            // Errores específicos del servidor
            responseMessage.style.color = "red";
            responseMessage.textContent = data.message || "No se pudo eliminar la cita.";
        }
    } catch (error) {
        // Manejo de errores en la conexión
        responseMessage.style.color = "red";
        responseMessage.textContent = "Error en la conexión. Verifica tu conexión a internet o inténtalo más tarde.";
    }
});
