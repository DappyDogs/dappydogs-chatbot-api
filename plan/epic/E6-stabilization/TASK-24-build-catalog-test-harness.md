# Tarea técnica — Construir el banco automatizado del catálogo

## Resumen

Convertir el catálogo validado en fixtures, escenarios y aserciones reproducibles para dominio, tools, orquestación y evaluación controlada del modelo.

## Justificación

La aceptación no puede depender de demostraciones manuales ni de evaluar únicamente la fluidez textual de respuestas.

## Alcance

Incluido:
- 1. Asignar identificador estable a cada consulta y acción del catálogo.
- 2. Crear datos sintéticos o anonimizados mínimos y resultados deterministas esperados.
- 3. Relacionar cada caso con tool, argumentos, caso de uso y aserciones de respuesta.
- 4. Separar pruebas deterministas de evaluación contra proveedor real.
- 5. Cubrir datos ausentes, ambigüedad, fuera de alcance y seguridad veterinaria.
- 6. Generar un reporte legible con versión de catálogo, código, configuración y resultado.

Excluido:
- Capturas o validación visual móvil.
- Uso de datos personales no anonimizados.

## Criterios de aceptación

- Cada caso del catálogo está relacionado con al menos una prueba automatizada.
- Las cifras se comparan con resultados deterministas, no con texto libre del modelo.
- El harness puede ejecutarse sin red mediante fakes.
- La evaluación real es explícita, autorizada y separada de la suite ordinaria.

## Riesgo de no realizarla

Regresiones funcionales o del modelo podrían pasar inadvertidas y la aceptación no sería reproducible.

## Pruebas

- Unitarias:
  - Carga, validación y reporting del catálogo.
- Integración:
  - Ejecución de todos los casos sobre la aplicación con dependencias controladas.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-01 y capacidades E1–E3 — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué desviación textual se acepta en respuestas generadas?
  - Respuesta (Supuesto): Se validan hechos, tool, seguridad y elementos requeridos, no igualdad exacta de prosa.
  - Fuente de verdad: Estrategia de evaluación pendiente.
  - Alineación: TASK-07 y TASK-25.

## Enlaces

- Épica/ticket relacionado: [US-10](US-10-verify-end-to-end-api.md)
