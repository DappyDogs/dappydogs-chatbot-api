# Tarea técnica — Modelar operaciones pendientes y propuestas editables

## Resumen

Implementar el agregado que conserva una propuesta de salud validada hasta su edición, confirmación, cancelación o expiración.

## Justificación

La confirmación debe ejecutar un payload estable y revisado, no reinterpretar el mensaje original ni confiar en datos arbitrarios del cliente.

## Alcance

Incluido:
- 1. Definir estados, transiciones, propiedad, versión, expiración y schema de propuesta.
- 2. Convertir la salida tipada del modelo en una propuesta normalizada sin persistir dominio.
- 3. Generar identificadores opacos y vincular la operación a usuario y conversación.
- 4. Permitir edición mediante una nueva versión completamente validada.
- 5. Invalidar confirmaciones de versiones obsoletas.
- 6. Implementar cancelación y expiración sin efectos de dominio.
- 7. Definir almacenamiento, TTL y limpieza de operaciones consumidas.

Excluido:
- Renderizado de la tarjeta móvil.
- Persistencia final del registro.

## Criterios de aceptación

- Crear o editar una propuesta no modifica `healthRecords`.
- Solo el propietario puede consultar, editar, cancelar o confirmar su operación.
- Las versiones obsoletas y expiradas se rechazan de forma estable.
- El payload normalizado es suficiente para confirmar sin volver a invocar al modelo.

## Riesgo de no realizarla

Una confirmación podría persistir datos distintos de los revisados o ser reutilizada por otra cuenta.

## Pruebas

- Unitarias:
  - Máquina de estados, versiones, validación y reloj.
- Integración:
  - Persistencia y aislamiento de operaciones pendientes.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-08 y TASK-15 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Dónde se almacenan y cuánto duran las operaciones pendientes?
  - Respuesta (Supuesto): Almacén server-side con TTL configurable; tecnología y duración pendientes.
  - Fuente de verdad: ADR de confirmación pendiente.
  - Alineación: TASK-18.

## Enlaces

- Épica/ticket relacionado: [US-07](US-07-confirm-health-writes.md)
