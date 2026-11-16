# Tarea técnica — Soportar actualizaciones confirmadas de registros

## Resumen

Extender el flujo de propuestas para modificar registros existentes con control de versión y detección de concurrencia.

## Justificación

El alcance incluye actualizar cuidados, pero una modificación no debe sobrescribir cambios concurrentes ni aceptar un identificador de otra cuenta.

## Alcance

Incluido:
- 1. Cargar el registro actual dentro del ámbito autenticado y proyectar su versión.
- 2. Crear una propuesta de cambios explícitos sin sustituir campos no mencionados.
- 3. Permitir edición y revalidación de la propuesta.
- 4. Confirmar mediante precondición sobre la versión del registro origen.
- 5. Detectar conflicto y solicitar nueva revisión si el registro cambió.
- 6. Conservar auditoría de actualización sin guardar conversación ni prompt.
- 7. Cubrir cancelación, idempotencia y acceso cruzado.

Excluido:
- Borrado conversacional de registros salvo aprobación expresa.
- Historial clínico de versiones.

## Criterios de aceptación

- Solo se modifican los campos presentes y validados en la propuesta confirmada.
- Un registro cambiado después de la propuesta no se sobrescribe silenciosamente.
- Un identificador ajeno no revela existencia ni permite operación pendiente.
- Reintentos de la misma actualización son idempotentes.

## Riesgo de no realizarla

Las actualizaciones podrían perder datos concurrentes o modificar registros ajenos.

## Pruebas

- Unitarias:
  - Diffs, validación parcial y conflictos de versión.
- Integración:
  - Actualización transaccional, concurrencia y aislamiento.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-16, TASK-17 y TASK-18 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Se permite eliminar registros desde el chatbot?
  - Respuesta (Supuesto): No está incluido explícitamente; requiere decisión de producto antes de añadirlo.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: Catálogo TASK-01.

## Enlaces

- Épica/ticket relacionado: [US-07](US-07-confirm-health-writes.md)
