function toggleEntrenadas() {
    const list = document.getElementById("entrenadas-list");
    if (list.style.display === "none" || list.style.display === "") {
        list.style.display = "block"; // Muestra la lista
    } else {
        list.style.display = "none"; // Oculta la lista
    }
}