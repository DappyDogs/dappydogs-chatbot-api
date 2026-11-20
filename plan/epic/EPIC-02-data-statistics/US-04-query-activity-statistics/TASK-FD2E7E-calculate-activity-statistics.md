# Tarea técnica — Calcular estadísticas deterministas de actividad

## Trazabilidad en Milano

- Código: `FD2E7E`.
- Story Points: 5.

## Resumen

Implementar servicios puros para totales, promedios, actividad semanal y mensual y comparativas básicas.

## Justificación

Los cálculos deben ser verificables y no depender del modelo, con contratos explícitos para periodos, unidades y datos vacíos.

## Alcance

Incluido:
1. Definir zona horaria, límites inclusivos/exclusivos y primer día de semana.
2. Calcular suma de distancia y duración, número de paseos y promedios acordados.
3. Implementar periodos semanales y mensuales con reloj inyectable.
4. Implementar únicamente las comparativas incluidas en el catálogo.
5. Definir semántica para periodo vacío, periodo parcial y divisor cero.
6. Mantener unidades canónicas y separar su formateo localizado.
7. Crear fixtures sintéticos para cambios de mes, año y horario.

Excluido:
- Tendencias, rachas, logros, rankings y recomendaciones.
- Cálculo mediante prompts.

## Criterios de aceptación

- Los resultados son deterministas para la misma entrada, reloj y zona horaria.
- Los límites de periodo se prueban con instantes exactos y cambios de calendario.
- Un periodo vacío produce un resultado explícito sin división por cero.
- Los valores coinciden con cálculos independientes del catálogo de pruebas.

## Riesgo de no realizarla

El modelo podría inventar o calcular de forma inconsistente las métricas de actividad.

## Pruebas

- Unitarias:
  - Totales, promedios, periodos, comparativas y casos vacíos.
- Integración:
  - Servicio sobre rutas normalizadas del repositorio.
- La funcionalidad existente no debe verse afectada (regresión).
