document.getElementById('get_keypoint').addEventListener('click', async () => {
    const loadingScreen = document.getElementById('loading-screen');
    try {
        loadingScreen.style.display = 'flex';
        const url = '/core/entrenamiento/get_keypoints'; // URL para la vista en Django
        const result = await fetchGet(url);

        if (result.ok) {
            console.log("Todo bien", result.data); // Muestra los datos de respuesta
        } else {
            console.error("Error:", result.data);
        }
    }catch (error) {
        console.error("Error en la petición:", error);
    } finally {
        // Ocultar la pantalla de carga después de que termine todo
        loadingScreen.style.display = 'none';
    }
});