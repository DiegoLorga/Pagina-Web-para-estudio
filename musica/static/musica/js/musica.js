document.addEventListener("DOMContentLoaded", function () {
    const pistas = [
        { archivo: "Música instrumental.mp3", nombre: "Música instrumental" },
        { archivo: "Ruido blanco.mp3", nombre: "Ruido blanco" },
        { archivo: "Sonido de lluvia.mp3", nombre: "Sonido de lluvia" },
        { archivo: "Studio Ghibli.mp3", nombre: "Studio Ghibli" }
    ];

    let indiceActual = 0;
    const audio = document.getElementById("audio");
    const nombre = document.getElementById("nombreCancion");
    const source = document.getElementById("audioSource");

    const btnReproducir = document.getElementById("reproducirBtn");
    const iconoReproducir = btnReproducir.querySelector("i");
    const btnAnterior = document.getElementById("anteriorBtn");
    const btnSiguiente = document.getElementById("siguienteBtn");

    function cargarPista(indice) {
        const pista = pistas[indice];
        source.src = `/static/musica/canciones/${pista.archivo}`;
        nombre.textContent = pista.nombre;
        audio.load();
        audio.play();
        actualizarIcono(true);
    }

    function actualizarIcono(estaReproduciendo) {
        iconoReproducir.classList.remove("fa-play", "fa-pause");
        iconoReproducir.classList.add(estaReproduciendo ? "fa-pause" : "fa-play");
    }

    btnAnterior.addEventListener("click", () => {
        indiceActual = (indiceActual - 1 + pistas.length) % pistas.length;
        cargarPista(indiceActual);
    });

    btnSiguiente.addEventListener("click", () => {
        indiceActual = (indiceActual + 1) % pistas.length;
        cargarPista(indiceActual);
    });

    btnReproducir.addEventListener("click", () => {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause();
        }
    });

    audio.addEventListener("play", () => actualizarIcono(true));
    audio.addEventListener("pause", () => actualizarIcono(false));

    audio.addEventListener("ended", () => {
        indiceActual = (indiceActual + 1) % pistas.length;
        cargarPista(indiceActual);
    });
});
