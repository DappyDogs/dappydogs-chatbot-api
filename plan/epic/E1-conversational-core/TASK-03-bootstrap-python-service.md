# Tarea técnica — Crear las fundaciones del servicio Python

## Resumen

Establecer el paquete Python 3.14, la estructura modular, configuración de calidad y aplicación HTTP mínima sobre la que se desarrollará la API.

## Justificación

El repositorio no contiene código, metadata de dependencias, tests ni configuración ejecutable. Las demás tareas necesitan una base reproducible y validada.

## Alcance

Incluido:
- 1. Crear `pyproject.toml` con versión, runtime y grupos de dependencias.
- 2. Crear el layout `src/dappydogs_chatbot_api` y los límites `api`, `application`, `domain`, `ports`, `adapters`, `normalization` y `settings`.
- 3. Seleccionar y configurar framework HTTP, Ruff, pytest y type checker.
- 4. Implementar settings tipados con fallo temprano y `.env.example` sin secretos.
- 5. Crear liveness, readiness inicial, error base y fixture de aplicación.
- 6. Alinear Makefile y comandos de validación.

Excluido:
- Integraciones reales con Firebase o el modelo.
- Endpoints funcionales del chatbot.

## Criterios de aceptación

- El entorno local instala el proyecto de forma editable con dependencias de desarrollo.
- Liveness responde sin depender de servicios externos y readiness tiene contrato explícito.
- Formato, lint, tipos y tests se ejecutan mediante comandos documentados.
- Los módulos internos no dependen todavía de SDKs externos fuera de adapters.

## Riesgo de no realizarla

Las capacidades crecerían sin límites arquitectónicos, tooling reproducible ni autoridad de configuración.

## Pruebas

- Unitarias:
  - Settings válidos e inválidos.
- Integración:
  - Arranque y endpoints de salud con cliente de pruebas.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- Decisión de framework y runtime cloud — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué framework HTTP y type checker se adoptan?
  - Respuesta (Supuesto): Se elegirán por compatibilidad con Python 3.14, tipado, streaming y runtime cloud.
  - Fuente de verdad: ADR técnico pendiente.
  - Alineación: TASK-05 y TASK-06.

## Enlaces

- Épica/ticket relacionado: [US-02](US-02-secure-api-access.md)
