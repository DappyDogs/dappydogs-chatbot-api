# Tarea técnica — Definir el contrato de telemetría del servidor

## Trazabilidad en Milano

- Código: `FD2E9A`.
- Story Points: 3.

## Resumen

Diseñar una taxonomía versionada de eventos y dimensiones permitidas para observar la API sin registrar contenido sensible ni identificadores de alta cardinalidad.

## Justificación

El discovery requiere métricas desde el primer día, pero una instrumentación improvisada podría filtrar mensajes, datos de salud o tokens y producir agregados inconsistentes.

## Alcance

Incluido:
1. Definir eventos para peticiones, capacidades, aclaraciones, propuestas, confirmaciones, errores, seguridad y cuotas.
2. Especificar propiedades obligatorias, opcionales, enumeraciones, versión y política de evolución.
3. Prohibir explícitamente mensajes, instrucciones y respuestas del modelo, tokens, ubicaciones, correos electrónicos y contenido de salud.
4. Definir identificadores pseudónimos o agregación previa cuando se necesiten usuarios activos.
5. Acordar retención, granularidad temporal y autoridad del evento.
6. Diseñar deduplicación y correlación sin exponer datos personales.
7. Asignar cada evento a un único productor: API/Firestore o aplicación/Firebase Analytics.
8. Definir el esquema versionado de `chatbotTelemetryEvents` y `chatbotMetricsDaily` con marcas temporales de servidor, identificador técnico, versión y dimensiones cerradas.

Excluido:
- Implementación de la vista visual.
- Eventos exclusivos de interfaz móvil.
- Implementación de esos eventos en los repositorios iOS y Android.

## Criterios de aceptación

- Cada métrica requerida puede derivarse de eventos documentados.
- El esquema rechaza propiedades no declaradas y contenido sensible conocido.
- La cardinalidad de dimensiones está acotada.
- Evolución, retención y autoridad están documentadas antes de producción.
- El catálogo permite reconciliar Firestore y Analytics sin sumar dos veces el mismo hecho.

## Riesgo de no realizarla

La telemetría podría incumplir privacidad, resultar costosa de consultar o no permitir calcular las métricas acordadas.

## Pruebas

- Unitarias:
  - Validación de esquemas y detectores de datos prohibidos.
- Integración:
  - Serialización de las nuevas colecciones y compatibilidad del catálogo con Firebase Analytics.
- La funcionalidad existente no debe verse afectada (regresión).
