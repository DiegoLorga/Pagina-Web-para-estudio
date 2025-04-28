// Info date
const dateNumber = document.getElementById('dateNumber');
const dateText = document.getElementById('dateText');
const dateMonth = document.getElementById('dateMonth');
const dateYear = document.getElementById('dateYear');

// Tasks Container
const tasksContainer = document.getElementById('tasksContainer');

// Arreglo para guardar tareas
let tasks = [];

const setDate = () => {
    const date = new Date();
    dateNumber.textContent = date.toLocaleString('es', { day: 'numeric' });
    dateText.textContent = date.toLocaleString('es', { weekday: 'long' });
    dateMonth.textContent = date.toLocaleString('es', { month: 'short' });
    dateYear.textContent = date.toLocaleString('es', { year: 'numeric' });
};

// Cargar tareas desde localStorage
const loadTasks = () => {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
    }
};

// Guardar tareas en localStorage
const saveTasks = () => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
};

// Crear la estructura HTML de una tarea
const createTaskElement = (taskObj) => {
    const task = document.createElement('div');
    task.classList.add('task', 'roundBorder');

    // Nuevo: hacer un contenedor interior para distribuir el texto y el select
    const taskContent = document.createElement('div');
    taskContent.classList.add('taskContent');

    const taskText = document.createElement('span');
    taskText.textContent = taskObj.text;

    const taskSelect = document.createElement('select');
    taskSelect.classList.add('taskState', 'roundBorder');

    const statuses = ['En proceso', 'Completa', 'Incompleta', 'Cancelada'];
    statuses.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.textContent = status;
        if (taskObj.status === status) {
            option.selected = true;
        }
        taskSelect.appendChild(option);
    });

    taskSelect.addEventListener('change', (e) => {
        taskObj.status = e.target.value;
        setTaskColor(task, taskObj.status);
        saveTasks();
        renderTasks();
    });

    setTaskColor(task, taskObj.status);

    // Agregamos el texto y el select al contenedor interior
    taskContent.appendChild(taskText);
    taskContent.appendChild(taskSelect);

    // Agregamos el contenedor a la tarea
    task.appendChild(taskContent);

    return task;
};


// Definir el color según el estado
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

// Función para agregar una nueva tarea
const addNewTask = event => {
    event.preventDefault();
    const { value } = event.target.taskText;
    if (!value) return;

    const newTask = {
        text: value,
        status: 'Incompleta'
    };

    tasks.unshift(newTask);
    saveTasks();
    renderTasks();
    event.target.reset();
};

// Ordenar las tareas por estado (incompleta, en proceso, cancelada, completa)
const sortTasks = () => {
    const priority = {
        'Incompleta': 0,
        'En proceso': 1,
        'Cancelada': 2,
        'Completa': 3
    };
    tasks.sort((a, b) => priority[a.status] - priority[b.status]);
};

// Renderizar todas las tareas
const renderTasks = () => {
    tasksContainer.innerHTML = '';
    sortTasks();
    tasks.forEach(taskObj => {
        const taskElement = createTaskElement(taskObj);
        tasksContainer.appendChild(taskElement);
    });
};

setDate();
loadTasks();
renderTasks();
