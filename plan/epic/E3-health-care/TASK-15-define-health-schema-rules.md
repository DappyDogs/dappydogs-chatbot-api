# Tarea técnica — Definir el esquema, índices y reglas de healthRecords

## Resumen

Formalizar y desplegar el contrato versionado de `Users/{uid}/healthRecords` con validación, índices y reglas estrictas.

## Justificación

La colección es nueva, contiene información sensible sobre cuidados y debe soportar consultas y evolución sin permitir escrituras directas no autorizadas.

## Alcance

Incluido:
- 1. Cerrar campos, enums, opcionalidad, tamaños, fechas y reglas específicas por tipo.
- 2. Añadir identificador, schema version, timestamps server-side, origen e idempotencia.
- 3. Definir una estrategia extensible para futura asociación a perro sin afirmar soporte actual.
- 4. Diseñar índices para listados por tipo, fecha y próxima fecha.
- 5. Escribir reglas: lectura del propio usuario según contrato y escrituras únicamente por el servicio.
- 6. Versionar configuración Firestore y probar reglas en emulador.
- 7. Definir compatibilidad y migración ante futuras versiones.

Excluido:
- Recordatorios y datos clínicos no acordados.
- Migración multi-perro.

## Criterios de aceptación

- El schema rechaza combinaciones inválidas y propiedades desconocidas.
- Las reglas impiden accesos cruzados y escrituras directas del cliente.
- Las consultas previstas disponen de índices versionados.
- La evolución futura está definida sin introducir campos especulativos no validados.

## Riesgo de no realizarla

Los datos quedarían inconsistentes, inseguros o imposibles de consultar y evolucionar de forma controlada.

## Pruebas

- Unitarias:
  - Validación de cada tipo y combinación inválida.
- Integración:
  - Reglas e índices con emulador y usuarios cruzados.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-01, TASK-02 y decisión de campos — debe completarse antes de empezar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Las fechas se almacenan como `Timestamp` y qué zona representa una fecha sin hora?
  - Respuesta (Supuesto): Deben distinguirse fecha civil y timestamp; contrato pendiente.
  - Fuente de verdad: ADR de datos pendiente.
  - Alineación: TASK-16 y TASK-17.

## Enlaces

- Épica/ticket relacionado: [US-06](US-06-query-health-records.md)
