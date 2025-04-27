function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
  let calendar;

  const initCalendar = () => {
    const calendarEl = document.getElementById('calendar');

    calendar = new FullCalendar.Calendar(calendarEl, {
      locale: 'es',
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'agregarEventoBtn prev,next today',
        center: 'title',
        right: 'dayGridMonth timeGridWeek timeGridDay'
      },
      customButtons: {
        agregarEventoBtn: {
          text: '+ Agregar evento',
          click: function () {
            const modal = new bootstrap.Modal(document.getElementById('formModal'));
            modal.show();
          }
        }
      },
      events: [
        { title: 'Tarea de Matemáticas', start: '2025-04-20' },
        { title: 'Revisión de Proyecto', start: '2025-04-23' }
      ]
    });

    calendar.render();

    // 🔽 Cambiar estilo al botón "Agregar evento"
    const botonAgregar = document.querySelector('.fc-agregarEventoBtn-button');
    if (botonAgregar) {
      botonAgregar.classList.remove('fc-button', 'fc-button-primary');
      botonAgregar.classList.add('btn', 'btn-success', 'me-2');
      botonAgregar.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';

      botonAgregar.addEventListener('mouseover', () => {
        botonAgregar.style.transform = 'scale(1.05)';
        botonAgregar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
      });

      botonAgregar.addEventListener('mouseout', () => {
        botonAgregar.style.transform = 'scale(1)';
        botonAgregar.style.boxShadow = 'none';
      });
    }
  };

  // Renderizar calendario cuando se abre el modal
  const calendarModal = document.getElementById('calendarModal');
  calendarModal.addEventListener('shown.bs.modal', function () {
    if (!calendar) {
      initCalendar();
    }
  });

  // Manejo del formulario de evento
  document.getElementById('eventoForm').addEventListener('submit', function (e) {
    e.preventDefault();
    console.log("usuarioId en JS antes de enviar:", usuarioId);  // 👀 AQUI

    const datos = {
      usuarioid: usuarioId, // ya viene del backend
      titulo: document.getElementById('titulo').value,
      descripcion: document.getElementById('descripcion').value,
      fecha_evento: document.getElementById('fecha_evento').value,
      importante: document.getElementById('importante').checked
    };
    

    console.log('Evento enviado:', datos);

    // Cierra el modal del formulario
    const modal = bootstrap.Modal.getInstance(document.getElementById('formModal'));
    modal.hide();
    this.reset();
  });
});

// Manejo del formulario de evento
document.getElementById('eventoForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const usuarioid = usuarioId;  // 🔥 ya viene de Django, no necesitas pedirlo del input
  const titulo = document.getElementById('titulo').value.trim();
  const descripcion = document.getElementById('descripcion').value.trim();
  const fecha_evento = document.getElementById('fecha_evento').value;
  const importante = document.getElementById('importante').checked;

  let errores = [];

  // Validación manual antes de enviar
  if (!usuarioid) errores.push('El campo "Usuario ID" es obligatorio.');
  if (!titulo) errores.push('El campo "Título" es obligatorio.');
  if (!descripcion) errores.push('El campo "Descripción" es obligatorio.');
  if (!fecha_evento) errores.push('Debes seleccionar una fecha para el evento.');

  if (errores.length > 0) {
    Swal.fire({
      icon: 'error',
      title: 'Campos incompletos',
      html: errores.map(err => `<p>${err}</p>`).join(''),
      confirmButtonColor: '#dc3545'
    });
    return;
  }

  // Si todo es válido, envía el fetch
  fetch('/api/eventos/crear/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      usuarioid,
      titulo,
      descripcion,
      fecha_evento,
      importante
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.id) {
      Swal.fire({
        icon: 'success',
        title: '¡Evento creado!',
        text: 'Tu evento ha sido guardado exitosamente.',
        confirmButtonColor: '#198754'
      });

      const modal = bootstrap.Modal.getInstance(document.getElementById('formModal'));
      modal.hide();
      e.target.reset();
    } else {
      // Mostrar errores enviados desde Django
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: data.error || 'No se pudo crear el evento.',
        confirmButtonColor: '#dc3545'
      });
    }
  })
  .catch(err => {
    console.error(err);
    Swal.fire({
      icon: 'error',
      title: 'Error de red',
      text: 'No se pudo conectar con el servidor.',
      confirmButtonColor: '#dc3545'
    });
  });
});

