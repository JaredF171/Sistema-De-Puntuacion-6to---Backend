"""
Servicio sencillo para generar feedback asistido.

No llama a un LLM real para evitar dependencias externas en test/CI, pero
estructura el texto como lo haría un asistente. Si quieres integrar un
proveedor (Gemini, OpenAI, etc.), puedes extender esta función y usar
la misma interfaz.
"""
from typing import Dict, Optional


def build_feedback(puntaje: float, kpis: Optional[Dict[str, float]] = None, comentario: str = "") -> str:
    """Construye un texto breve de retroalimentación."""
    kpis = kpis or {}
    promedio_kpi = round(sum(kpis.values()) / len(kpis), 2) if kpis else puntaje

    bloques = []
    bloques.append(f"Evaluación general: {puntaje}/20.")
    if kpis:
        bloques.append(f"Promedio de KPI: {promedio_kpi}/20 en {len(kpis)} criterios.")
    if comentario:
        bloques.append(f"Comentario del supervisor: {comentario.strip()}")

    if puntaje >= 18:
        conclusion = "Desempeño sobresaliente: mantener el nivel y compartir buenas prácticas con el equipo."
    elif puntaje >= 15:
        conclusion = "Buen desempeño: consolidar fortalezas y seguir mejorando puntualidad y documentación."
    elif puntaje >= 12:
        conclusion = "Desempeño aceptable: reforzar áreas de oportunidad identificadas y pedir retroalimentación frecuente."
    else:
        conclusion = "Desempeño por debajo de lo esperado: definir un plan de mejora con objetivos claros y seguimiento cercano."

    bloques.append(conclusion)
    return " ".join(bloques)
