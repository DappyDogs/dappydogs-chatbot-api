# Épica — E3 · Registro de salud y cuidados

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** registrar y consultar vacunas, desparasitaciones, medicamentos y citas desde el chat
**PARA** conservar información estructurada de los cuidados de mi perro

## Contexto y justificación

La información de salud y cuidados no existe actualmente. Debe crearse una estructura nueva y aislada, con esquema versionado, nombres estables, tipos temporales correctos, reglas e índices estrictos y un flujo que impida cualquier escritura sin revisión y confirmación del usuario. La heterogeneidad de las colecciones heredadas no justifica reproducir sus patrones en esta persistencia nueva.

## Valor esperado / métricas de éxito

- El 100 % de escrituras requiere una propuesta válida y confirmación explícita.
- Los reintentos de una confirmación no crean duplicados.
- Ningún usuario puede leer o modificar registros de otra cuenta.
- Los registros participan en el borrado de cuenta.

## Alcance

Incluido:
- Contrato versionado de `healthRecords`, índices y reglas.
- Tipos diferenciados para fechas civiles e instantes, timestamps gestionados por servidor y validación cerrada por tipo de registro.
- Consulta de registros y próximas fechas como datos.
- Propuesta, edición, confirmación, actualización y cancelación.
- Idempotencia, expiración y concurrencia.
- Integración con borrado de cuenta.

Excluido:
- Diagnóstico o validación clínica.
- Recordatorios proactivos y notificaciones.
- Soporte efectivo para varios perros por cuenta.
- Reutilización de claves dinámicas, timestamps textuales, flags enteros o documentos agregadores heredados.
- Limpieza o migración de cualquier colección existente.

## Riesgos y dependencias

- Campos mínimos por tipo todavía no acordados — (Impacto: alto)
- Reglas, índices y proceso de borrado pendientes de verificar — (Impacto: alto)
- Integración móvil de edición y confirmación — (Impacto: medio)
- Convivencia segura con el documento `Users` heredado sin acoplar el esquema nuevo a sus variantes — (Impacto: medio)

## Hitos (opcional)

- Primera propuesta y confirmación de salud operativa — 04/12/2026

## Correspondencia de entrega

- Código de Milano: `FD2E00`.
- Estado de Milano verificado el 18 de noviembre de 2026: `backlog`.
- Asignación de Milano: Sprint 2 y el hito compartido de consultas, estadísticas y primer registro de salud.
- La integración con el borrado de cuenta y la confirmación móvil son dependencias transversales obligatorias, aunque su ejecución pertenezca también a sistemas externos.
