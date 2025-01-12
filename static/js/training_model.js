document.getElementById('training_model').addEventListener('click', async () => {
    console.log("Botón presionado");
    const loadingScreen = document.getElementById('loading-screen');

    try {
        // Mostrar la pantalla de carga
        loadingScreen.style.display = 'flex';

        const url = '/core/entrenamiento/training_model'; // URL para la vista en Django
        const response = await fetch(url);

        if (response.ok) {
            const data = await response.json(); // Asegúrate de que tu backend devuelva JSON
            console.log("Todo bien", data); // Muestra los datos de respuesta
        } else {
            console.error("Error:", response.statusText);
        }
    } catch (error) {
        console.error("Error en la petición:", error);
    } finally {
        // Ocultar la pantalla de carga después de que termine todo
        loadingScreen.style.display = 'none';
    }
});