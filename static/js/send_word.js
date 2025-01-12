var video = document.getElementById('video');
var botonIniciar = document.getElementById('start_training');
var botonDetener = document.getElementById('stop_training');
var botonizquierdo = document.getElementById('btn-left');
var botonderecho = document.getElementById('btn-right');
var form = document.getElementById("temporal_content");


document.getElementById('start_training').addEventListener('click', async function()  {
    var palabra = document.getElementById('Palabra').value;
    if (palabra !=''){
        const data = { word : palabra }; 
        const url = '/core/entrenamiento/start_camera'; 

        const response = await fetchPost(url, data); // Llamada a fetchPost

        if (response.ok) {
            video.src = '/core/entrenamiento/video_feed'; // Configura el flujo de video
            form.style.display = "none";
            botonIniciar.style.display = 'none';
            botonizquierdo.style.display = 'none';
            botonderecho.style.display = 'none';
            botonDetener.style.display = 'inline';

            startProgressUpdate();

        } else {
            console.error('Error starting camera:', response.data);
        }
    }
})


function stopVideo() {
    fetch('/core/entrenamiento/stop_camera')
        .then(response => {
            if (response.ok) {
                return response.json(); 
            } else {
                console.error("Error stopping camera");
                throw new Error('Error stopping camera');
            }
        })
        .then(data => {
            video.src = '';
            form.style.display = "block";
            botonIniciar.style.display = 'inline';
            botonizquierdo.style.display = 'inline';
            botonderecho.style.display = 'inline';
            botonDetener.style.display = 'none';

            if (window.progressInterval) {
                clearInterval(window.progressInterval);
            }
    
            // Reiniciar el texto de progreso
            document.getElementById('progress').innerText = '';
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}

function startProgressUpdate() {
    const progressInterval = setInterval(async () => {
        try {
            const response = await fetch('/core/entrenamiento/get_progress');
            if (response.ok) {
                const data = await response.json();
                if (data.error) {
                    document.getElementById('progress').innerText = "Error: " + data.error;
                } else {
                    document.getElementById('progress').innerText =
                        `Capturando imágenes para la palabra: ${data.current_word} (Sample ${data.current_sample})`;
                }
            } else {
                console.error('Error fetching progress');
                clearInterval(progressInterval); // Detén el intervalo si hay un error
            }
        } catch (error) {
            console.error('Error fetching progress:', error);
            clearInterval(progressInterval); // Detén el intervalo si hay un error
        }
    }, 2000);

    // Guarda el intervalo en un atributo para detenerlo más tarde
    window.progressInterval = progressInterval;
}









