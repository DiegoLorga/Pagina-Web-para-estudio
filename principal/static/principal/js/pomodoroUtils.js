function buildPomodoroPlan(totalTime) {
    const plan = [];
    const pomodoroDuration = 25 * 60; // 25 min
    const shortBreak = 5 * 60;
    const longBreak = 15 * 60;

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

module.exports = { buildPomodoroPlan };
