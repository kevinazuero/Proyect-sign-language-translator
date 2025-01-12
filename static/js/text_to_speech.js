document.getElementById('volumeButton').addEventListener('click', async () => {
    const texto = document.getElementById('cuadro_texto').value;
    const data = { text: texto };

    const response = await fetchPost(`/core/text_speech`, data);
    if (response.ok) {
        console.log('Texto enviado correctamente');
    } else {
        console.error('Error al enviar el texto', response.data.message);
    }
});