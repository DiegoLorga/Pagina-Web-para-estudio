document.addEventListener('DOMContentLoaded', () => {
    const timer = document.getElementById('timer');
    const startBtn = document.getElementById('startBtn');
    const resetBtn = document.getElementById('resetBtn');
    const openModalBtn = document.getElementById('openModalBtn');
    const timeSelect = document.getElementById('timeSelect');
    const setTimeBtn = document.getElementById('setTimeBtn');
    const breakCount = document.getElementById('breakCount');
    const nextSessionMsg = document.getElementById('nextSession');
    const sound = new Audio('/static/principal/sounds/notificacion.mp3');

    let fullPlan = [];
    let currentIndex = 0;
    let interval = null;
    let time = 1800; // 30 minutos inicial
    let isPaused = false;

    // fullPlan = buildPomodoroPlan(1800);
    fullPlan = buildPomodoroPlanTest();

    time = fullPlan.length > 0 ? fullPlan[0].duration : 1800;
    updateTimer();

    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    function sendNotification(message) {
        if (Notification.permission === "granted") {
            new Notification(message);
            sound.play();
        }
    }
    function buildPomodoroPlanTest() {
        return [
            { type: 'study', duration: 25 },
            { type: 'break', duration: 10 }
        ];
    }
   /*  
   function updateTimer() { /////////////////codigo real ///////////////////////
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    if (time <= 0) {
        clearInterval(interval);
        interval = null;

        const session = fullPlan[currentIndex];

        if (session) {
            sendNotification(
                session.type === 'study'
                    ? "¡Pomodoro terminado! Hora de descansar."
                    : "¡Descanso terminado! Hora de concentrarte."
            );

            if (session.type === 'study') {
                fetch('/principal/aumentar-racha/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        console.log(' Racha actualizada:', data.racha);

                        //  Actualizar imagen
                        const rachaImg = document.getElementById('rachaImagen');
                        if (rachaImg) {
                            rachaImg.src = "/static/principal/image/rachaActiva.png";
                        }

                        //  Actualizar texto de racha
                        const rachaTexto = document.getElementById('rachaTexto');
                        if (rachaTexto) {
                            rachaTexto.textContent = data.racha;
                        }
                    } else {
                        console.warn(' Error al aumentar la racha:', data.error);
                    }
                })
                .catch(error => {
                    console.error(' Error en la petición:', error);
                });
            }
        }

        currentIndex++;
        if (currentIndex < fullPlan.length) {
            startSession();
        } else {
            document.getElementById('timer').style.display = 'none';  // Oculta el cronómetro
            const mensajeFinal = document.getElementById('mensajeFinal');
            mensajeFinal.textContent = "¡Fin!";
            mensajeFinal.style.display = 'block';
            startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
            nextSessionMsg.textContent = "";
            resetBtn.style.display = "none";
        }
    } else {
        time--;
    }
}

     */


    ////////////////////////////tester/////////////////////////////////////////////
    function updateTimer() {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
        if (time <= 0) {
            clearInterval(interval);
            interval = null;
    
            const session = fullPlan[currentIndex];
    
            if (session) {
                sendNotification(
                    session.type === 'study'
                        ? "Pomodoro de prueba terminado."
                        : "Descanso de prueba terminado."
                );
    
                if (session.type === 'study') {
                    fetch('/aumentar-racha/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({})
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("Respuesta del servidor:", data);
    
                        if (data.ok) {
                            // ✅ Cambiar imagen a racha activa
                            const img = document.getElementById('rachaImagen');
                            if (img) {
                                img.src = "/static/principal/image/rachaActiva.png";
                                console.log("✅ Imagen cambiada a racha activa");
                            } else {
                                console.warn("⚠️ No se encontró el elemento con id='rachaImagen'");
                            }
    
                            // ✅ Actualizar número de días de racha
                            const rachaTexto = document.getElementById('rachaTexto');
                            if (rachaTexto) {
                                console.log(" Texto de racha actualizado:", data.racha);
                                rachaTexto.textContent = data.racha;
                                console.log(" Texto de racha actualizado:", data.racha);
                            } else {
                                console.warn(" No se encontró el elemento con id='rachaTexto'");
                            }
                        } else {
                            console.warn(' Error al aumentar la racha (fetch ok):', data.error);
                        }
                    })
                    .catch(error => {
                        console.error(' Error en fetch:', error);
                    });
                }
            }
    
            currentIndex++;
            if (currentIndex < fullPlan.length) {
                startSession();
            } else {
                document.getElementById('timer').style.display = 'none';
                const mensajeFinal = document.getElementById('mensajeFinal');
                mensajeFinal.textContent = "¡Prueba completada!";
                mensajeFinal.style.display = 'block';
                startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
                nextSessionMsg.textContent = "";
                resetBtn.style.display = "none";
            }
        } else {
            time--;
        }
    }
    
    
    
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return '';
    }
    
    function startSession() {
        const session = fullPlan[currentIndex];
        if (!isPaused) {
            time = session.duration;
        }
        updateTimer();
        interval = setInterval(updateTimer, 1000);
        startBtn.innerHTML = '<i class="fas fa-pause"></i> <span></span>';
        isPaused = false;

        const next = fullPlan[currentIndex + 1];
        if (next) {
            if (next.type === 'break') {
                nextSessionMsg.textContent = `A continuación: descanso de ${Math.floor(next.duration / 60)} minutos.`;
            } else {
                nextSessionMsg.textContent = `A continuación: sesión de concentración.`;
            }
        } else {
            nextSessionMsg.textContent = "";
        }
    }

    function buildPomodoroPlan(totalTime) {
        const plan = [];
        const pomodoroDuration = 25 * 60; //  25 minutos
        const shortBreak = 5 * 60;         //  5 minutos descanso
        const longBreak = 15 * 60;          //  15 minutos largo

        let remaining = totalTime;
        let count = 0;

        while (remaining >= pomodoroDuration) {
            plan.push({ type: 'study', duration: pomodoroDuration });
            remaining -= pomodoroDuration;
            count++;

            if (remaining >= longBreak && count % 4 === 0) {
                plan.push({ type: 'break', duration: longBreak });
                remaining -= longBreak;
            } else if (remaining >= shortBreak && remaining >= 5 * 60) {
                plan.push({ type: 'break', duration: shortBreak });
                remaining -= shortBreak;
            }
        }

        if (remaining > 0) {
            plan.push({ type: 'study', duration: remaining });
        }

        return plan;
    }

    startBtn.addEventListener('click', () => {
        if (!interval && fullPlan.length > 0) {
            if (isPaused) {
                interval = setInterval(updateTimer, 1000);
                startBtn.innerHTML = '<i class="fas fa-pause"></i> <span></span>';
                isPaused = false;
                resetBtn.style.display = "none";
            } else {
                startSession();
            }
        } else if (interval) {
            clearInterval(interval);
            interval = null;
            startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
            isPaused = true;
            resetBtn.style.display = "inline-block";
        }
    });

    resetBtn.addEventListener('click', () => {
        clearInterval(interval);
        interval = null;
        isPaused = false;
        currentIndex = 0;
        time = 1800;
        fullPlan = buildPomodoroPlan(1800);
        timer.textContent = "30:00";
        startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
        nextSessionMsg.textContent = "";
        resetBtn.style.display = "none";
    });

    openModalBtn.addEventListener('click', () => {
        const modalInstance = new bootstrap.Modal(document.getElementById('timeModal'));
        modalInstance.show();
        timeSelect.dispatchEvent(new Event('change'));
    });

    timeSelect.addEventListener('change', () => {
        const selectedTime = parseInt(timeSelect.value);
        let pomodoros = Math.floor(selectedTime / (25 * 60));
        let descansos = pomodoros - 1;
        if (descansos < 0) descansos = 0;

        breakCount.textContent = `Tendrás ${pomodoros} Pomodoro${pomodoros > 1 ? 's' : ''} y ${descansos} descanso${descansos !== 1 ? 's' : ''}.`;
    });

    setTimeBtn.addEventListener('click', () => {
        clearInterval(interval);
        interval = null;
        currentIndex = 0;
        const selectedTime = parseInt(timeSelect.value);
        fullPlan = buildPomodoroPlan(selectedTime);
        time = fullPlan.length > 0 ? fullPlan[0].duration : selectedTime;
        updateTimer();
        startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
        document.getElementById('timer').style.display = 'block';
        document.getElementById('mensajeFinal').style.display = 'none';        

        const modal = bootstrap.Modal.getInstance(document.getElementById('timeModal'));
        modal.hide();
    });

    timeSelect.dispatchEvent(new Event('change'));
});
