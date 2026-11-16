# Épica — E2 · Consulta de datos y estadísticas

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** consultar el perfil de mi perro y su actividad mediante lenguaje natural
**PARA** obtener respuestas correctas sin localizar manualmente la información en la aplicación

## Contexto y justificación

Los datos existen en `Users` y `Routes`, pero presentan fechas textuales, catálogos numéricos y posibles diferencias de unidades entre plataformas. La API debe normalizarlos y calcular las estadísticas mediante código.

## Valor esperado / métricas de éxito

- Las consultas del catálogo devuelven cifras coincidentes con cálculos independientes sobre datos controlados.
- Los registros inválidos o incompletos no distorsionan silenciosamente las estadísticas.
- Ninguna respuesta incluye datos de otra cuenta.

## Alcance

Incluido:
- Modelos canónicos y normalización de `Users` y `Routes`.
- Consultas de perfil y paseos por periodo.
- Totales, promedios, actividad semanal y mensual y comparativas básicas.
- Tools estructuradas y respuestas fundamentadas.

Excluido:
- Paseos en curso, ubicación, rachas, logros y clasificaciones.
- Comparativas avanzadas, tendencias y mensajes motivacionales.

## Historias de usuario incluidas

- [US-04 — Consultar el perfil normalizado del perro](US-04-query-dog-profile.md)
- [US-05 — Consultar paseos y estadísticas de actividad](US-05-query-activity-statistics.md)

## Riesgos y dependencias

- Unidades de timestamps pendientes de verificar con datos reales — (Impacto: alto)
- Catálogos numéricos canónicos no disponibles todavía — (Impacto: medio)
- Datos históricos heterogéneos o incompletos — (Impacto: medio)

## Hitos (opcional)

- Catálogo de consultas y estadísticas operativo — 04/12/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué zona horaria y límites definen semanas y meses?
  - Respuesta (Supuesto): Pendiente de decisión de producto y datos del proyecto Firebase.
  - Fuente de verdad: Catálogo funcional pendiente.
  - Alineación: US-05.
- ¿Qué comparativas se consideran básicas?
  - Respuesta (Supuesto): Solo las expresamente incluidas en el catálogo validado.
  - Fuente de verdad: Informe de discovery v1.0 y catálogo pendiente.
  - Alineación: US-05.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E1 — Núcleo conversacional](../E1-conversational-core/EPIC.md)
