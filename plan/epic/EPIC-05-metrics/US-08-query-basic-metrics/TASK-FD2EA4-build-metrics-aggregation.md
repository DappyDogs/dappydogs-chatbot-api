# Tarea técnica — Construir la agregación de métricas básicas

## Trazabilidad en Milano

- Código: `FD2EA4`.
- Story Points: 5.

## Resumen

Transformar eventos válidos en agregados por periodo para usuarios activos, conversaciones, mensajes, capacidades, registros, errores y uso del proveedor.

## Justificación

Consultar eventos crudos sería ineficiente, expondría más detalle del necesario y dificultaría definiciones consistentes de producto.

## Alcance

Incluido:
1. Definir formalmente cada métrica, su unidad, periodo, zona horaria y fuente.
2. Implementar agregación incremental desde `chatbotTelemetryEvents` hacia `chatbotMetricsDaily`, con reproceso idempotente por periodo.
3. Deduplicar eventos por identidad técnica y gestionar eventos tardíos.
4. Mantener dimensiones cerradas por tipo de consulta y resultado.
5. Calcular el coste estimado a partir de unidades de uso reales y una tabla versionada de precios por proveedor/modelo; declarar ausencia cuando falten unidades o precio aplicable.
6. Aplicar retención y permisos a eventos y agregados.
7. Incorporar los agregados móviles necesarios desde la exportación o integración acordada de Firebase Analytics sin copiar contenido ni eventos individuales innecesarios.

Excluido:
- Cohortes, tendencias avanzadas y analítica individual.
- Cálculos sobre contenido conversacional.

## Criterios de aceptación

- Cada agregado puede reconciliarse con un conjunto controlado de eventos.
- Duplicados y eventos tardíos siguen una política determinista.
- No se necesita leer mensajes o registros de salud para calcular métricas.
- Los periodos vacíos y datos parciales se representan explícitamente.
- El coste estimado conserva proveedor, modelo, versión de tarifa y periodo, sin asociarlo a contenido conversacional.

## Riesgo de no realizarla

La vista podría producir cifras inconsistentes, costosas o derivadas de datos sensibles.

## Pruebas

- Unitarias:
  - Fórmulas, periodos, deduplicación y eventos tardíos.
- Integración:
  - Agregación sobre Firestore, reconciliación con Analytics y reproceso idempotente.
- La funcionalidad existente no debe verse afectada (regresión).
