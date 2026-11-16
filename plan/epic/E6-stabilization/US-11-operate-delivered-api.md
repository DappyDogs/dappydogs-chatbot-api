# Historia de usuario — Operar y mantener la API entregada

## Objetivo

**COMO** equipo responsable de operación
**NECESITO** despliegue reproducible, configuración validada y documentación técnica
**PARA** diagnosticar, mantener y recuperar el servicio de forma segura

## Contexto

La entrega incluye arquitectura, despliegue, configuración y operación. El servicio debe identificar su versión, separar secretos, exponer salud útil y disponer de procedimientos verificables.

## Alcance

Incluido:
- Configuración de despliegue reproducible y secretos.
- Liveness, readiness, logs, métricas y alertas acordadas.
- Runbooks de despliegue, rollback, incidentes y rotación.
- Documentación técnica y traspaso.

Excluido:
- Operación de las aplicaciones móviles y tiendas.
- Soporte de sistemas heredados no consumidos por la API.

## Criterios de aceptación

- **AC.01.** Caso: despliegue limpio
  Dado un entorno autorizado y secretos configurados;
  Cuando se ejecuta el procedimiento documentado;
  Entonces se despliega una versión identificable y saludable sin pasos implícitos.
- **AC.02.** Caso: configuración inválida
  Dada una variable obligatoria ausente o incoherente;
  Cuando inicia el servicio;
  Entonces falla de forma temprana con un diagnóstico sanitizado.
- **AC.03.** Caso: traspaso
  Dada la versión entregada;
  Cuando el equipo operador sigue los runbooks;
  Entonces puede verificar salud, localizar errores, rotar secretos y ejecutar rollback.

## Casos límite / fallos

- Dependencia degradada, secreto rotado, despliegue parcial y rollback de esquema incompatible.

## Pruebas

- Unitarias:
  - Validación de configuración.
- Integración:
  - Readiness y dependencias en entorno controlado.
- E2E:
  - Smoke test posterior al despliegue y rollback ensayado.
- Visuales:
  - No aplica.

## Dependencias

- US-10 y decisiones operativas — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Quién recibe alertas y autoriza despliegues y rollback?
  - Respuesta (Supuesto): Debe definirse durante el traspaso antes de producción.
  - Fuente de verdad: Modelo operativo pendiente.
  - Alineación: TASK-26 y TASK-27.

## Enlaces

- Épica: [E6](EPIC.md)
- Tareas: [TASK-26](TASK-26-harden-deployment-operations.md), [TASK-27](TASK-27-produce-technical-handoff.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Runtime, despliegue y operación pendientes.
