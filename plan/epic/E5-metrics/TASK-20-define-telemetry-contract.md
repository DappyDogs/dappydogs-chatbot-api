# Tarea técnica — Definir el contrato de telemetría server-side

## Resumen

Diseñar una taxonomía versionada de eventos y dimensiones permitidas para observar la API sin registrar contenido sensible ni identificadores de alta cardinalidad.

## Justificación

El discovery requiere métricas desde el primer día, pero una instrumentación improvisada podría filtrar mensajes, datos de salud o tokens y producir agregados inconsistentes.

## Alcance

Incluido:
- 1. Definir eventos para peticiones, capacidades, aclaraciones, propuestas, confirmaciones, errores, seguridad y cuotas.
- 2. Especificar propiedades obligatorias, opcionales, enums, versión y política de evolución.
- 3. Prohibir explícitamente mensajes, prompts, respuestas, tokens, ubicaciones, emails y contenido de salud.
- 4. Definir identificadores pseudónimos o agregación previa cuando se necesiten usuarios activos.
- 5. Acordar retención, granularidad temporal y autoridad del evento.
- 6. Diseñar deduplicación y correlación sin exponer datos personales.

Excluido:
- Implementación del dashboard.
- Eventos exclusivos de interfaz móvil.

## Criterios de aceptación

- Cada métrica requerida puede derivarse de eventos documentados.
- El schema rechaza propiedades no declaradas y contenido sensible conocido.
- La cardinalidad de dimensiones está acotada.
- Evolución, retención y autoridad están documentadas antes de producción.

## Riesgo de no realizarla

La telemetría podría incumplir privacidad, resultar costosa de consultar o no permitir calcular las métricas acordadas.

## Pruebas

- Unitarias:
  - Validación de schemas y detectores de datos prohibidos.
- Integración:
  - Serialización y compatibilidad con el backend seleccionado.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- Política de privacidad y decisión de backend — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Cómo se calculan usuarios activos sin persistir `uid` en analítica?
  - Respuesta (Supuesto): Mediante identificador pseudónimo rotatorio o agregación server-side; requiere revisión de privacidad.
  - Fuente de verdad: Decisión de privacidad pendiente.
  - Alineación: TASK-22.

## Enlaces

- Épica/ticket relacionado: [US-08](US-08-instrument-api-usage.md)
