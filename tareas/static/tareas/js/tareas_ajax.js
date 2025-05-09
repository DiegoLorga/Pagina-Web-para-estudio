document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("taskForm");
    const taskInput = document.getElementById("taskInput");
    const tasksContainer = document.getElementById("tasksContainer");

    if (!taskForm || !taskInput || !tasksContainer) return;

    const ordenarTareas = () => {
        const tareas = Array.from(tasksContainer.children);
        const ordenEstados = {
            0: 1, // Incompleta (al final)
            2: 0, // En proceso
            1: 2, // Completa
            3: 3  // Cancelada (más abajo)
        };

        tareas.sort((a, b) => {
            const estadoA = parseInt(a.querySelector("select").value);
            const estadoB = parseInt(b.querySelector("select").value);
            return ordenEstados[estadoA] - ordenEstados[estadoB];
        });

        tasksContainer.innerHTML = "";
        tareas.forEach(t => tasksContainer.appendChild(t));
    };

    ordenarTareas(); // ordena tareas al cargar

    taskForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(taskForm);

        const response = await fetch(taskForm.getAttribute('data-url'), {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            tasksContainer.insertAdjacentHTML("beforeend", data.html);
            taskForm.reset();
            ordenarTareas(); // ordena después de insertar
        } else {
            alert("Error al crear la tarea.");
        }
    });
});

function actualizarEstado(selectElement) {
    const estado = selectElement.value;
    const tareaId = selectElement.dataset.id;

    fetch(`/tareas/actualizar/${tareaId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ estado: estado })
    })
    .then(response => {
        if (!response.ok) throw new Error("Error en la respuesta del servidor.");
        return response.json();
    })
    .then(data => {
        const colorMap = {
            "0": "#dc3545",  // Incompleta
            "1": "#ABC252",  // Completa
            "2": "#ffc107",  // En proceso
            "3": "#6c757d"   // Cancelada
        };
        const taskElement = selectElement.closest('.task');
        taskElement.style.backgroundColor = colorMap[estado];

        // Reordenar sin perder info ni eventos
        const container = document.getElementById("tasksContainer");
        container.appendChild(taskElement); // mover al final primero
        ordenarTareas(); // reordenar todo
    })
    .catch(error => {
        console.error("Error al actualizar tarea:", error);
        alert("Ocurrió un error al actualizar la tarea.");
    });
}

// Mover la función fuera para que esté disponible globalmente
function ordenarTareas() {
    const tasksContainer = document.getElementById("tasksContainer");
    const tareas = Array.from(tasksContainer.children);
    const ordenEstados = {
        0: 3,
        2: 2,
        1: 1,
        3: 4
    };

    tareas.sort((a, b) => {
        const estadoA = parseInt(a.querySelector("select").value);
        const estadoB = parseInt(b.querySelector("select").value);
        return ordenEstados[estadoA] - ordenEstados[estadoB];
    });

    tasksContainer.innerHTML = "";
    tareas.forEach(t => tasksContainer.appendChild(t));
}
