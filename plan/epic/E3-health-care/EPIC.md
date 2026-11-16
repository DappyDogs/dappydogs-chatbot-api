# Épica — E3 · Registro de salud y cuidados

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** registrar y consultar vacunas, desparasitaciones, medicamentos y citas desde el chat
**PARA** conservar información estructurada de los cuidados de mi perro

## Contexto y justificación

La información de salud y cuidados no existe actualmente. Debe crearse una estructura nueva y aislada, con reglas estrictas y un flujo que impida cualquier escritura sin revisión y confirmación del usuario.

## Valor esperado / métricas de éxito

- El 100 % de escrituras requiere una propuesta válida y confirmación explícita.
- Los reintentos de una confirmación no crean duplicados.
- Ningún usuario puede leer o modificar registros de otra cuenta.
- Los registros participan en el borrado de cuenta.

## Alcance

Incluido:
- Contrato versionado de `healthRecords`, índices y reglas.
- Consulta de registros y próximas fechas como datos.
- Propuesta, edición, confirmación, actualización y cancelación.
- Idempotencia, expiración y concurrencia.
- Integración con borrado de cuenta.

Excluido:
- Diagnóstico o validación clínica.
- Recordatorios proactivos y notificaciones.
- Soporte efectivo para varios perros por cuenta.

## Historias de usuario incluidas

- [US-06 — Consultar registros de salud y cuidados](US-06-query-health-records.md)
- [US-07 — Registrar y actualizar cuidados con confirmación](US-07-confirm-health-writes.md)

## Riesgos y dependencias

- Campos mínimos por tipo todavía no acordados — (Impacto: alto)
- Reglas, índices y proceso de borrado pendientes de verificar — (Impacto: alto)
- Integración móvil de edición y confirmación — (Impacto: medio)

## Hitos (opcional)

- Primera propuesta y confirmación de salud operativa — 04/12/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué campos son obligatorios y opcionales para cada tipo?
  - Respuesta (Supuesto): El discovery propone tipo, título, fecha, próxima fecha, dosis, frecuencia, notas y auditoría; falta validación final.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: US-06 y US-07.
- ¿Cómo se representa la futura asociación a varios perros?
  - Respuesta (Supuesto): El esquema debe ser extensible sin afirmar soporte multi-perro actual.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-15.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E1 — Núcleo conversacional](../E1-conversational-core/EPIC.md)
