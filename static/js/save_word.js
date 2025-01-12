document.getElementById('clean').addEventListener('click', async function() {
    var palabra = document.getElementById('cuadro_texto').value;
    if (palabra !=''){
        const data = {
            word: palabra
        };
        const response = await fetchPost(`/core/historial/save_word`, data)
        if (!response.ok) return alert("error en los datos"+response.data.message)
    }
});



