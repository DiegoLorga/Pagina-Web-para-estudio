const { setTaskColor, sortTasks } = require('./listaUtils');

describe('setTaskColor', () => {
    test('debe aplicar color correcto según estado', () => {
        const task = { style: {} };

        setTaskColor(task, 'Completa');
        expect(task.style.backgroundColor).toBe('#ABC252');

        setTaskColor(task, 'En proceso');
        expect(task.style.backgroundColor).toBe('#ffc107');

        setTaskColor(task, 'Incompleta');
        expect(task.style.backgroundColor).toBe('#dc3545');

        setTaskColor(task, 'Cancelada');
        expect(task.style.backgroundColor).toBe('#6c757d');

        setTaskColor(task, 'otro');
        expect(task.style.backgroundColor).toBe('var(--primary)');
    });
});

describe('sortTasks', () => {
    test('debe ordenar tareas por prioridad', () => {
        const tasks = [
            { text: 'A', status: 'Completa' },
            { text: 'B', status: 'Incompleta' },
            { text: 'C', status: 'En proceso' },
            { text: 'D', status: 'Cancelada' }
        ];

        sortTasks(tasks); // <-- Solo llamas

        expect(tasks[0].status).toBe('Incompleta');
        expect(tasks[1].status).toBe('En proceso');
        expect(tasks[2].status).toBe('Cancelada');
        expect(tasks[3].status).toBe('Completa');
    });
});