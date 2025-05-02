from django.test import TestCase
import pytest

# Esta función simula el buildPomodoroPlan de JS
def build_pomodoro_plan(total_time):
    plan = []
    pomodoro_duration = 25 * 60  # 25 minutos
    short_break = 5 * 60         # 5 minutos
    long_break = 15 * 60         # 15 minutos

    remaining = total_time
    count = 0

    while remaining >= pomodoro_duration:
        plan.append({"type": "study", "duration": pomodoro_duration})
        remaining -= pomodoro_duration
        count += 1

        if remaining >= long_break and count % 4 == 0:
            plan.append({"type": "break", "duration": long_break})
            remaining -= long_break
        elif remaining >= short_break and remaining >= 5 * 60:
            plan.append({"type": "break", "duration": short_break})
            remaining -= short_break

    if remaining > 0:
        plan.append({"type": "study", "duration": remaining})

    return plan

# Ahora las pruebas

def test_build_pomodoro_plan_30_minutes():
    total_time = 30 * 60  # 30 minutos
    plan = build_pomodoro_plan(total_time)

    assert len(plan) >= 1
    assert plan[0]["type"] == "study"
    assert plan[0]["duration"] == 25 * 60  # Primer Pomodoro
    assert plan[-1]["type"] in ["study", "break"]  
    assert plan[-1]["duration"] <= 5 * 60  # Sobrante máximo 5 minutos

def test_build_pomodoro_plan_2_hours():
    total_time = 120 * 60  # 2 horas
    plan = build_pomodoro_plan(total_time)

    study_sessions = [s for s in plan if s["type"] == "study"]
    break_sessions = [s for s in plan if s["type"] == "break"]

    assert len(study_sessions) >= 4
    assert len(break_sessions) >= 3
    assert plan[0]["type"] == "study"
    assert plan[1]["type"] == "break"
