document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const citaId = button.getAttribute('data-cita-id');
            const confirmDelete = confirm('¿Estás seguro de que deseas eliminar esta cita?');

            if (confirmDelete) {
                try {
                    const response = await fetch(`/borrar_cita/${citaId}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        alert('Cita eliminada con éxito.');
                        document.getElementById(`cita-${citaId}`).remove();
                    } else {
                        alert('Hubo un problema al eliminar la cita.');
                    }
                } catch (error) {
                    console.error('Error al eliminar la cita:', error);
                    alert('Hubo un error al intentar eliminar la cita.');
                }
            }
        });
    });
});
