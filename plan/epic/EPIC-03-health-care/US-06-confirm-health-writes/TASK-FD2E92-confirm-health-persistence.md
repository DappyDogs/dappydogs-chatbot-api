# Tarea técnica — Confirmar y persistir registros con idempotencia

## Trazabilidad en Milano

- Código: `FD2E92`.
- Story Points: 8.

## Resumen

Implementar el comando autenticado que consume una operación pendiente vigente y crea el registro de salud exactamente una vez.

## Justificación

Reintentos móviles, timeouts y concurrencia pueden duplicar registros si confirmación y persistencia no forman una transición atómica e idempotente.

## Alcance

Incluido:
1. Definir el endpoint/comando de confirmación con operation ID, versión e idempotency key.
2. Cargar y autorizar la operación por principal autenticado.
3. Validar estado, versión, expiración y esquema vigente.
4. Crear el registro y consumir la operación mediante transacción o precondición atómica.
5. Devolver el resultado previo ante repeticiones equivalentes.
6. Rechazar reutilización con payload o clave contradictorios.
7. Emitir eventos sanitizados de resultado.
8. Persistir fechas, marcas temporales, enumeraciones y metadatos exactamente con el esquema versionado de salud, sin conversiones heredadas ni campos adicionales del modelo.

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
