document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("modificar-form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const numeroDeCita = document.getElementById("numeroDeCita").value;
        const nombre = document.getElementById("nombre").value;
        const fecha = document.getElementById("fecha").value;
        const hora = document.getElementById("hora").value;
        const descripcion = document.getElementById("descripcion").value;

        try {
            const response = await fetch(`/modificar/cita/${numeroDeCita}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nombre,
                    fecha,
                    hora,
                    descripcion
                })
            });

            if (response.ok) {
                alert("Cita actualizada correctamente.");
                window.location.href = "/menu_cita";
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error || "No se pudo actualizar la cita."}`);
            }
        } catch (error) {
            alert("Error de conexión. Intenta nuevamente.");
        }
    });
});
