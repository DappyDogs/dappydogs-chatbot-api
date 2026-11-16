# Historia de usuario — Consultar registros de salud y cuidados

## Objetivo

**COMO** usuario autenticado
**NECESITO** consultar los cuidados registrados de mi perro
**PARA** recuperar vacunas, desparasitaciones, medicamentos y citas mediante el chatbot

## Contexto

Los registros no existen actualmente. La nueva subcolección debe ofrecer un contrato tipado, reglas estrictas, consultas autorizadas y compatibilidad con el borrado de cuenta.

## Alcance

Incluido:
- Esquema versionado, reglas e índices.
- Repositorio filtrado por usuario.
- Listados, filtros por tipo y próximas fechas.
- Participación en el borrado de cuenta.

Excluido:
- Recordatorios proactivos y validación clínica.
- Soporte multi-perro efectivo.

## Criterios de aceptación

- **AC.01.** Caso: consulta autorizada
  Dado un usuario con registros propios;
  Cuando solicita un tipo o próxima fecha soportados;
  Entonces recibe exclusivamente sus registros normalizados y ordenados según contrato.
- **AC.02.** Caso: aislamiento
  Dado un identificador de registro perteneciente a otra cuenta;
  Cuando se intenta consultar;
  Entonces la API no devuelve ni confirma su existencia.
- **AC.03.** Caso: borrado de cuenta
  Dado el flujo aprobado de eliminación de usuario;
  Cuando se elimina la cuenta;
  Entonces sus registros de salud se eliminan conforme al contrato de retención.

## Casos límite / fallos

- Colección vacía, fechas pasadas, próxima fecha ausente, registros heredados y paginación.

## Pruebas

- Unitarias:
  - Validación y ordenación de registros.
- Integración:
  - Reglas, índices, aislamiento y borrado con emulador.
- E2E:
  - Consultas de salud del catálogo.
- Visuales:
  - No aplica.

## Dependencias

- E0, US-02 y campos de salud acordados — debe completarse antes de empezar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué contrato de borrado y retención se aplica?
  - Respuesta (Supuesto): Los registros se eliminan con la cuenta; falta verificar el flujo técnico existente.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-16.

## Enlaces

- Épica: [E3](EPIC.md)
- Tareas: [TASK-15](TASK-15-define-health-schema-rules.md), [TASK-16](TASK-16-build-health-read-repository.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Esquema de salud pendiente.
