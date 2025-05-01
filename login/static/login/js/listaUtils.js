// listaUtils.js

const setTaskColor = (taskElement, status) => {
    switch (status) {
        case 'Completa':
            taskElement.style.backgroundColor = '#ABC252'; // Verde
            break;
        case 'En proceso':
            taskElement.style.backgroundColor = '#ffc107'; // Amarillo
            break;
        case 'Incompleta':
            taskElement.style.backgroundColor = '#dc3545'; // Rojo
            break;
        case 'Cancelada':
            taskElement.style.backgroundColor = '#6c757d'; // Gris
            break;
        default:
            taskElement.style.backgroundColor = 'var(--primary)';
    }
};

const sortTasks = (tasks) => {
    const priority = {
        'Incompleta': 0,
        'En proceso': 1,
        'Cancelada': 2,
        'Completa': 3
    };
    tasks.sort((a, b) => priority[a.status] - priority[b.status]);
    return tasks;
};

module.exports = { setTaskColor, sortTasks };