# Tarea técnica — Construir la agregación de métricas básicas

## Resumen

Transformar eventos válidos en agregados por periodo para usuarios activos, conversaciones, mensajes, capacidades, registros, errores y uso del proveedor.

## Justificación

Consultar eventos crudos sería ineficiente, expondría más detalle del necesario y dificultaría definiciones consistentes de producto.

## Alcance

Incluido:
- 1. Definir formalmente cada métrica, su unidad, periodo, zona horaria y fuente.
- 2. Diseñar agregación incremental o bajo demanda según volumen verificado.
- 3. Deduplicar eventos por identidad técnica y gestionar eventos tardíos.
- 4. Mantener dimensiones cerradas por tipo de consulta y resultado.
- 5. Representar metadatos de proveedor ausentes sin inventar estimaciones.
- 6. Aplicar retención y permisos al almacén agregado.

Excluido:
- Cohortes, tendencias avanzadas y analítica individual.
- Cálculos sobre contenido conversacional.

## Criterios de aceptación

- Cada agregado puede reconciliarse con un conjunto controlado de eventos.
- Duplicados y eventos tardíos siguen una política determinista.
- No se necesita leer mensajes o registros de salud para calcular métricas.
- Los periodos vacíos y datos parciales se representan explícitamente.

## Riesgo de no realizarla

La vista podría producir cifras inconsistentes, costosas o derivadas de datos sensibles.

## Pruebas

- Unitarias:
  - Fórmulas, periodos, deduplicación y eventos tardíos.
- Integración:
  - Agregación sobre el backend seleccionado y reconciliación controlada.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-20 y TASK-21 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué latencia de actualización necesita la vista?
  - Respuesta (Supuesto): Métricas no necesariamente en tiempo real; intervalo pendiente de decisión.
  - Fuente de verdad: Requisito operativo pendiente.
  - Alineación: TASK-23.

## Enlaces

- Épica/ticket relacionado: [US-09](US-09-query-basic-metrics.md)
