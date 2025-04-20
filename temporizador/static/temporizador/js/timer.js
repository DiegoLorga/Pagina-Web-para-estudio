// temporizador/static/temporizador/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const timer = document.getElementById('timer');
    const startBtn = document.getElementById('startBtn');
    let time = 1 * 60; // 20 minutos en segundos
    let interval;

    function updateTimer() {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (time <= 0) {
            clearInterval(interval);
            timer.textContent = "¡Fin!";
        } else {
            time--;
        }
    }

    startBtn.addEventListener('click', () => {
        if (!interval) {
            interval = setInterval(updateTimer, 1000);
            startBtn.textContent = "Pausar";
        } else {
            clearInterval(interval);
            interval = null;
            startBtn.textContent = "Iniciar";
        }
    });
});