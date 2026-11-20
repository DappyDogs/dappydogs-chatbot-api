# Tarea técnica — Modelar operaciones pendientes y propuestas editables

## Trazabilidad en Milano

- Código: `FD2E8E`.
- Story Points: 5.

## Resumen

Implementar el agregado que conserva una propuesta de salud validada hasta su edición, confirmación, cancelación o expiración.

## Justificación

La confirmación debe ejecutar un payload estable y revisado, no reinterpretar el mensaje original ni confiar en datos arbitrarios del cliente.

## Alcance

Incluido:
1. Definir estados, transiciones, propiedad, versión, expiración y esquema de propuesta.
2. Convertir la salida tipada del modelo en una propuesta normalizada sin persistir dominio.
3. Generar identificadores opacos y vincular la operación a usuario y conversación.
4. Permitir edición mediante una nueva versión completamente validada.
5. Invalidar confirmaciones de versiones obsoletas.
6. Implementar cancelación y expiración sin efectos de dominio.
7. Definir almacenamiento, TTL y limpieza de operaciones consumidas.
8. Diseñar el almacenamiento con campos estables, timestamps de servidor, `schemaVersion` y reglas propias, sin mapas de claves dinámicas.

Excluido:
- Renderizado de la tarjeta móvil.
- Persistencia final del registro.

## Criterios de aceptación

- Crear o editar una propuesta no modifica `healthRecords`.
- Solo el propietario puede consultar, editar, cancelar o confirmar su operación.
- Las versiones obsoletas y expiradas se rechazan de forma estable.
- El payload normalizado es suficiente para confirmar sin volver a invocar al modelo.
- La propuesta usa exactamente el contrato de salud vigente y no admite formatos temporales heredados.

## Riesgo de no realizarla

Una confirmación podría persistir datos distintos de los revisados o ser reutilizada por otra cuenta.

## Pruebas

- Unitarias:
  - Máquina de estados, versiones, validación y reloj.
- Integración:
  - Persistencia y aislamiento de operaciones pendientes.
- La funcionalidad existente no debe verse afectada (regresión).
