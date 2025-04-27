document.addEventListener('DOMContentLoaded', () => {
    const timer = document.getElementById('timer');
    const startBtn = document.getElementById('startBtn');
    const resetBtn = document.getElementById('resetBtn');
    const openModalBtn = document.getElementById('openModalBtn');
    const modal = document.getElementById('timeModal');
    const timeSelect = document.getElementById('timeSelect');
    const setTimeBtn = document.getElementById('setTimeBtn');
    const breakCount = document.getElementById('breakCount');
    const nextSessionMsg = document.getElementById('nextSession');
    const sound = new Audio('/static/temporizador/sounds/notificacion.mp3');


    let fullPlan = [];
    let currentIndex = 0;
    let interval = null;
    let time = 1800; // 30 minutos en segundos
    let isPaused = false;

    // Establecer 30 min como predeterminado al cargar
    fullPlan = buildPomodoroPlan(1800);
    time = fullPlan.length > 0 ? fullPlan[0].duration : 1800;
    updateTimer();
    //  Pide permiso para mostrar notificaciones
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    function sendNotification(message) {
        if (Notification.permission === "granted") {
            new Notification(message); 
            sound.play();
            
        }
    }

    function updateTimer() {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        if (time <= 0) {
            clearInterval(interval);
            interval = null;
            const session = fullPlan[currentIndex];
            // ⚡ Notificación al terminar la sesión actual
            if (session && session.type === 'study') {
                sendNotification("¡Pomodoro terminado! Hora de descansar.");
            } else if (session && session.type === 'break') {
                sendNotification("¡Descanso terminado! Hora de concentrarte.");
            }
            currentIndex++;
            if (currentIndex < fullPlan.length) {
                startSession();
            } else {
                timer.textContent = "¡Fin total!";
                startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
                nextSessionMsg.textContent = "";
                resetBtn.style.display = "none";
            }
        } else {
            time--;
        }
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
                const mins = Math.floor(next.duration / 60);
                nextSessionMsg.textContent = `A continuación: descanso de ${mins} minutos.`;
            } else {
                nextSessionMsg.textContent = `A continuación: sesión de concentración.`;
            }
        } else {
            nextSessionMsg.textContent = "";
        }
    }

    function buildPomodoroPlan(totalTime) {
        // const plan = [];
        // const pomodoroDuration = 5 * 60;
        // const shortBreak = 5 * 60;
        // const longBreak = 15 * 60;   


        const plan = [];
        const pomodoroDuration = 25; 
        const shortBreak = 5;        
        const longBreak = 15;         
        

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
        time = 1800; // Reiniciar a 30 minutos
        fullPlan = buildPomodoroPlan(1800);
        timer.textContent = "30:00";
        startBtn.innerHTML = '<i class="fas fa-play"></i> <span></span>';
        nextSessionMsg.textContent = "";
        resetBtn.style.display = "none";
    });

    openModalBtn.addEventListener('click', () => {
        modal.style.display = 'flex';
        timeSelect.dispatchEvent(new Event('change'));
    });

    timeSelect.addEventListener('change', () => {
        const selectedTime = parseInt(timeSelect.value);
        let pomodoros = 0;
        let descansos = 0;

        switch (selectedTime) {
            case 1800:
                pomodoros = 1; descansos = 1; break;
            case 3600:
                pomodoros = 2; descansos = 2; break;
            case 5400:
                pomodoros = 3; descansos = 3; break;
            case 7800:
                pomodoros = 4; descansos = 3; break;
            case 9600:
                pomodoros = 5; descansos = 4; break;
            case 11100:
                pomodoros = 6; descansos = 5; break;
            case 13200:
                pomodoros = 7; descansos = 6; break;
            case 14700:
                pomodoros = 8; descansos = 7; break;
            default:
                break;
        }

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
        nextSessionMsg.textContent = "";
        resetBtn.style.display = "none";
        modal.style.display = 'none';
    });

    timeSelect.dispatchEvent(new Event('change'));
});
