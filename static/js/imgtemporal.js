function temporalimg(event) {
    const input = event.target;
    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = function() {
        const preview = document.getElementById('imgperfil');
        preview.src = reader.result;
    };

    if (file) {
        reader.readAsDataURL(file);
    }
}