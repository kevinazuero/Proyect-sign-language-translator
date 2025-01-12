var video = document.getElementById('video');
var botonIniciar = document.getElementById('start');
var botonDetener = document.getElementById('boton1');
var cuadro_texto = document.getElementById('cuadro_texto')

cuadro_texto.value = " "

function startVideo() {
    fetch('/core/start_camera')
        .then(response => {
            if (response.ok) {
                video.src = '/core/video_feed';
                botonIniciar.style.display = 'none';
                botonDetener.style.display = 'inline';
            } else {
                console.error("Error starting camera");
            }
        });
}


function stopVideo() {
    fetch('/core/stop_camera')
        .then(response => {
            if (response.ok) {
                return response.json(); 
            } else {
                console.error("Error stopping camera");
                throw new Error('Error stopping camera');
            }
        })
        .then(data => {
            cuadro_texto.value += data.palabras_concatenadas
            video.src = '';
            botonIniciar.style.display = 'inline';
            botonDetener.style.display = 'none';
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}

