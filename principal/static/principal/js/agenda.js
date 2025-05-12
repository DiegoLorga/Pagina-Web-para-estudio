// Obtiene el token CSRF desde el meta tag del HTML
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Función para obtener una cookie por nombre (útil para CSRF si no se usa meta tag)
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

// Espera a que el DOM esté cargado
document.addEventListener('DOMContentLoaded', function () {
  let calendar; // Variable para almacenar la instancia del calendario

  // Inicializa el calendario con FullCalendar
  const initCalendar = () => {
    const calendarEl = document.getElementById('calendar');
  
    calendar = new FullCalendar.Calendar(calendarEl, {
      locale: 'es', // Idioma en español
      initialView: 'dayGridMonth', // Vista inicial
      allDayText: 'Eventos', // Texto para eventos de todo el día
      height: '700px',
      allDaySlot: true,
      slotMinTime: "00:00:00",
      slotMaxTime: "00:00:00",
      headerToolbar: {
        left: 'agregarEventoBtn prev,next today',
        center: 'title',
        right: 'dayGridMonth timeGridWeek timeGridDay'
      },
      buttonText: {
        today: 'Hoy',
        month: 'Mes',
        week: 'Semana',
        day: 'Día'
      },
      // Botón personalizado para agregar un evento
      customButtons: {
        agregarEventoBtn: {
          text: '+ Agregar evento',
          click: function () {
            const modal = new bootstrap.Modal(document.getElementById('formModal'));
            modal.show();
          }
        }
      },
    
      // Renderizado personalizado del contenido del evento
      eventContent: function(arg) {
        const viewType = arg.view.type;
        if (viewType === 'timeGridWeek' || viewType === 'timeGridDay') {
          const evento = arg.event;
          const isImportante = evento.extendedProps.importante;
      
          const contenedor = document.createElement('div');
          contenedor.style.padding = '10px';
          contenedor.style.borderRadius = '10px';
          contenedor.style.backgroundColor = isImportante ? '#ABC252' : '#d3d3d3';
          contenedor.style.border = `1px solid ${isImportante ? '#ABC252' : '#d3d3d3'}`;
          contenedor.style.color = '#000';
          contenedor.style.fontSize = '0.9rem';
          contenedor.style.lineHeight = '1.4';
          contenedor.style.whiteSpace = 'normal';
          contenedor.style.wordWrap = 'break-word';
          contenedor.style.height = '100%';
          contenedor.style.overflow = 'hidden';
      
          contenedor.innerHTML = `
  <div style="font-weight:bold; font-size:1rem; margin-bottom:6px;">
    ${isImportante ? '📍' : '📌'} ${evento.title}
  </div>
  <div style="margin-bottom:6px;">
    ${evento.extendedProps.descripcion}
  </div>
  <div style="font-size:0.75rem; font-style:italic; color:#333;">
    ${isImportante ? '🔥 Evento importante' : ''}
  </div>
`;

          return { domNodes: [contenedor] };
        }
        return true;
      }
    });
  
    calendar.render(); // Renderiza el calendario en el DOM
  };
  
  // Evento que se dispara cuando se abre el modal del calendario
  const calendarModal = document.getElementById('calendarModal');
  calendarModal.addEventListener('shown.bs.modal', function () {
    if (!calendar) {
      initCalendar(); // Inicializa si aún no existe
    }

    // Elimina cualquier fuente de eventos existente
    if (calendar.getEventSources().length > 0) {
      calendar.getEventSources().forEach(source => source.remove());
    }

    // Solicita los eventos del usuario al backend
    fetch('/eventos/usuario/')
      .then(res => res.json())
      .then(data => {
        const eventosFormateados = data.map(evt => ({
          title: evt.titulo,
          start: evt.fecha_evento,
          allDay: true,
          backgroundColor: evt.importante ? '#ABC252' : '#d3d3d3',
          borderColor: evt.importante ? '#ABC252' : '#d3d3d3',
          textColor: '#000',
          descripcion: evt.descripcion,
          importante: evt.importante
        }));
        calendar.addEventSource(eventosFormateados); // Agrega los eventos al calendario
      })
      .catch(err => {
        console.error("Error al obtener eventos del usuario:", err);
      });
  });

  // Maneja el envío del formulario para crear un evento
  document.getElementById('eventoForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Evita recarga de la página

    // Obtiene los valores del formulario
    const usuarioid = usuarioId;
    const titulo = document.getElementById('titulo').value.trim();
    const descripcion = document.getElementById('descripcion').value.trim();
    const fecha_evento = document.getElementById('fecha_evento').value;
    const importante = document.getElementById('importante').checked;

    let errores = [];

    // Validaciones básicas
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

    // Envío de datos al backend
    fetch('/eventos/crear/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
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
          // Éxito al guardar el evento
          Swal.fire({
            icon: 'success',
            title: '¡Evento creado!',
            text: 'Tu evento ha sido guardado exitosamentee.',
            confirmButtonColor: '#198754'
          }).then(() => {
            const formModal = bootstrap.Modal.getInstance(document.getElementById('formModal'));
            if (formModal) formModal.hide(); // Cierra el modal del formulario
            const calendarModal = bootstrap.Modal.getInstance(document.getElementById('calendarModal'));
            if (calendarModal) calendarModal.hide(); // Cierra el modal del calendario
            document.getElementById('eventoForm').reset(); // Limpia el formulario
          });
        } else {
          // Error devuelto por el servidor
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: data.error || 'No se pudo crear el evento.',
            confirmButtonColor: '#dc3545'
          });
        }
      })
      .catch(err => {
        // Error de red o conexión
        console.error(err);
        Swal.fire({
          icon: 'error',
          title: 'Error de red',
          text: 'No se pudo conectar con el servidor.',
          confirmButtonColor: '#dc3545'
        });
      });
  });
});
