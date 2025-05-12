from django.test import TestCase

# La función a probar: genera un plan Pomodoro basado en el tiempo total dado
def build_pomodoro_plan(total_time):
    plan = []
    pomodoro_duration = 25 * 60  # 25 minutos de estudio
    short_break = 5 * 60         # 5 minutos de descanso corto
    long_break = 15 * 60         # 15 minutos de descanso largo

    remaining = total_time  # Tiempo restante
    count = 0  # Contador de sesiones de estudio

    # Mientras haya tiempo suficiente para una sesión Pomodoro completa
    while remaining >= pomodoro_duration:
        plan.append({"type": "study", "duration": pomodoro_duration})  # Añade sesión de estudio
        remaining -= pomodoro_duration
        count += 1

        # Cada 4 sesiones se agrega un descanso largo si hay tiempo
        if remaining >= long_break and count % 4 == 0:
            plan.append({"type": "break", "duration": long_break})
            remaining -= long_break
        # Si no, se agrega un descanso corto si hay al menos 5 minutos
        elif remaining >= short_break and remaining >= 5 * 60:
            plan.append({"type": "break", "duration": short_break})
            remaining -= short_break

    # Si queda tiempo, se usa como una sesión final de estudio
    if remaining > 0:
        plan.append({"type": "study", "duration": remaining})

    return plan  # Devuelve la lista de sesiones

# Caso de prueba para la función build_pomodoro_plan
class PomodoroPlanTest(TestCase):

    # Prueba con 30 minutos (solo alcanza para 1 Pomodoro y posiblemente un descanso corto)
    def test_plan_with_30_minutes(self):
        total_time = 30 * 60
        plan = build_pomodoro_plan(total_time)

        self.assertGreaterEqual(len(plan), 1)  # Al menos debe haber una sesión
        self.assertEqual(plan[0]["type"], "study")  # La primera debe ser de estudio
        self.assertEqual(plan[0]["duration"], 25 * 60)  # Duración estándar
        self.assertIn(plan[-1]["type"], ["study", "break"])  # La última puede ser cualquiera
        self.assertLessEqual(plan[-1]["duration"], 5 * 60)  # Si hay descanso, no debe exceder 5 min

    # Prueba con 2 horas (debe incluir múltiples sesiones y descansos)
    def test_plan_with_2_hours(self):
        total_time = 120 * 60
        plan = build_pomodoro_plan(total_time)

        # Separa las sesiones de estudio y descanso
        study_sessions = [s for s in plan if s["type"] == "study"]
        break_sessions = [s for s in plan if s["type"] == "break"]

        self.assertGreaterEqual(len(study_sessions), 4)  # Al menos 4 sesiones de estudio
        self.assertGreaterEqual(len(break_sessions), 3)  # Al menos 3 descansos
        self.assertEqual(plan[0]["type"], "study")  # La primera siempre debe ser estudio
        self.assertEqual(plan[1]["type"], "break")  # La segunda generalmente será un descanso
