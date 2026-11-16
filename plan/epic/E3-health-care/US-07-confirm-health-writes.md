# Historia de usuario — Registrar y actualizar cuidados con confirmación

## Objetivo

**COMO** usuario autenticado
**NECESITO** revisar, corregir y confirmar un registro propuesto por el chatbot
**PARA** evitar que información incorrecta se guarde sin mi consentimiento

## Contexto

El modelo interpreta el mensaje, pero la API debe convertirlo en una propuesta tipada. La aplicación muestra y permite editar la tarjeta; solo una confirmación autenticada de la versión vigente puede persistir el registro.

## Alcance

Incluido:
- Operaciones pendientes tipadas, versionadas y con expiración.
- Edición y revalidación de propuestas.
- Confirmación, cancelación e idempotencia.
- Creación y actualización transaccional de registros.

Excluido:
- Diseño o implementación de la tarjeta móvil.
- Escrituras directas solicitadas por el modelo.

## Criterios de aceptación

- **AC.01.** Caso: propuesta sin confirmación
  Dado un mensaje que describe un cuidado;
  Cuando el modelo devuelve una propuesta válida;
  Entonces la API crea una operación pendiente y no modifica `healthRecords`.
- **AC.02.** Caso: confirmación válida
  Dada una operación vigente y perteneciente al usuario;
  Cuando confirma la versión actual;
  Entonces se persiste exactamente una vez el payload validado y se devuelve el resultado.
- **AC.03.** Caso: edición
  Dada una propuesta pendiente;
  Cuando el usuario corrige sus campos;
  Entonces se crea una versión validada y la versión anterior deja de ser confirmable.
- **AC.04.** Caso: repetición o concurrencia
  Dada una confirmación ya consumida;
  Cuando se repite o llega en paralelo;
  Entonces no se crea un duplicado y la respuesta mantiene semántica idempotente.

## Casos límite / fallos

- Operación expirada, cancelada, ajena, editada simultáneamente o con fecha/enum inválidos.

## Pruebas

- Unitarias:
  - Ciclo de estado, validación, versiones e idempotencia.
- Integración:
  - Transacciones y aislamiento con Firestore emulado.
- E2E:
  - Propuesta, edición, confirmación, repetición y cancelación.
- Visuales:
  - No aplica en este repositorio.

## Dependencias

- US-03 y US-06 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Cuál es la vida útil de una operación pendiente?
  - Respuesta (Supuesto): Debe ser configurable y suficientemente corta; valor pendiente.
  - Fuente de verdad: Decisión técnica pendiente.
  - Alineación: TASK-17.

## Enlaces

- Épica: [E3](EPIC.md)
- Tareas: [TASK-17](TASK-17-model-pending-operations.md), [TASK-18](TASK-18-confirm-health-persistence.md), [TASK-19](TASK-19-support-health-updates.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Confirmación e idempotencia pendientes.
