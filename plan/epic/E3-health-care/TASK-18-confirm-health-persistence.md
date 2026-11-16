# Tarea técnica — Confirmar y persistir registros con idempotencia

## Resumen

Implementar el comando autenticado que consume una operación pendiente vigente y crea el registro de salud exactamente una vez.

## Justificación

Reintentos móviles, timeouts y concurrencia pueden duplicar registros si confirmación y persistencia no forman una transición atómica e idempotente.

## Alcance

Incluido:
- 1. Definir el endpoint/comando de confirmación con operation ID, versión e idempotency key.
- 2. Cargar y autorizar la operación por principal autenticado.
- 3. Validar estado, versión, expiración y schema vigente.
- 4. Crear el registro y consumir la operación mediante transacción o precondición atómica.
- 5. Devolver el resultado previo ante repeticiones equivalentes.
- 6. Rechazar reutilización con payload o clave contradictorios.
- 7. Emitir eventos sanitizados de resultado.

Excluido:
- Envío de recordatorios o push.
- Diagnóstico de la información introducida.

## Criterios de aceptación

- Una confirmación válida crea exactamente un registro.
- Confirmaciones repetidas o concurrentes no crean duplicados.
- Operaciones ajenas, expiradas, canceladas o con versión obsoleta no escriben.
- Un fallo parcial no deja operación y registro en estados contradictorios.

## Riesgo de no realizarla

Los usuarios podrían generar duplicados o persistir operaciones no vigentes ante problemas de red.

## Pruebas

- Unitarias:
  - Decisiones de confirmación e idempotencia.
- Integración:
  - Transacciones, concurrencia, timeout simulado y reintentos con emulador.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-15 y TASK-17 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿La idempotency key la genera el cliente o la operación pendiente?
  - Respuesta (Supuesto): El servidor define la operación y el cliente aporta una clave de intento estable; contrato final pendiente.
  - Fuente de verdad: ADR de idempotencia pendiente.
  - Alineación: E4.

## Enlaces

- Épica/ticket relacionado: [US-07](US-07-confirm-health-writes.md)
