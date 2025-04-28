const { buildPomodoroPlan } = require('./pomodoroUtils'); // Ajusta la ruta si es necesario

describe('buildPomodoroPlan', () => {
    test('debe construir un plan correcto para 30 minutos', () => {
        const plan = buildPomodoroPlan(1800); // 30 minutos

        expect(plan.length).toBeGreaterThan(0);
        expect(plan[0].type).toBe('study');
        expect(plan[0].duration).toBe(1500); // 25 minutos

        // debería quedar una sesión corta después
        expect(plan[1].type).toBe('break');
        expect(plan[1].duration).toBe(300); // 5 minutos
    });

    test('debe incluir descansos largos después de 4 pomodoros', () => {
        const plan = buildPomodoroPlan(4 * (25 * 60 + 5 * 60) + 15 * 60);

        const longBreakFound = plan.find(session => session.type === 'break' && session.duration === 900);
        expect(longBreakFound).toBeDefined();
    });

    test('debe manejar tiempos menores a un pomodoro', () => {
        const plan = buildPomodoroPlan(600); // 10 minutos

        expect(plan.length).toBe(1);
        expect(plan[0].type).toBe('study');
        expect(plan[0].duration).toBe(600);
    });

    test('debe retornar un arreglo vacío si el tiempo es cero', () => {
        const plan = buildPomodoroPlan(0);

        expect(plan.length).toBe(0);
    });
});
