# Épica — E4 · Integración en iOS y Android

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** acceder al chatbot desde las aplicaciones iOS y Android
**PARA** utilizar las capacidades de la API dentro de la experiencia habitual de la aplicación

## Contexto y justificación

El discovery asigna esta épica a los repositorios móviles: pantalla, navegación, componentes visuales, tarjeta de confirmación, estados de carga y error, localización, App Check y publicación de versiones de prueba. Este repositorio únicamente proporciona y estabiliza el contrato API consumido por esas implementaciones.

## Valor esperado / métricas de éxito

- Ambas aplicaciones consumen el mismo contrato autenticado sin lógica de negocio duplicada.
- El flujo de propuesta, edición y confirmación funciona de extremo a extremo.
- Los errores, límites y estados de seguridad de la API pueden representarse de forma estable en ambos clientes.

## Alcance

Incluido:
- Coordinación y soporte del contrato API desde las épicas E1, E2 y E3.
- Compatibilidad del contrato con Firebase Auth, App Check, reintentos y confirmación móvil.

Excluido:
- Implementación de pantallas iOS o Android en este repositorio.
- Componentes visuales, navegación y localización móvil.
- Ramas móviles, TestFlight, Google Play y publicación en tiendas.

## Historias de usuario incluidas

No se crean historias ni tareas en este repositorio para E4. El trabajo ejecutable pertenece a los repositorios iOS y Android; cualquier ajuste del contrato API se planifica en la épica backend que sea responsable de la capacidad afectada.

## Riesgos y dependencias

- Contrato de streaming, reintentos y cancelación pendiente — (Impacto: alto)
- Activación coordinada de App Check — (Impacto: alto)
- Dependencia de la librería Android compilada — (Impacto: medio)

## Hitos (opcional)

- Contrato API integrado en versiones móviles de prueba — 11/12/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿La respuesta conversacional será completa o en streaming?
  - Respuesta (Supuesto): Pendiente de decisión conjunta con los equipos móviles.
  - Fuente de verdad: Contrato de integración todavía no aprobado.
  - Alineación: E1 y E6.
- ¿Cómo reintentan los clientes las confirmaciones?
  - Respuesta (Supuesto): Mediante una clave idempotente y una operación pendiente versionada; falta cerrar el contrato HTTP.
  - Fuente de verdad: Arquitectura propuesta en el contexto técnico.
  - Alineación: E3.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E1](../E1-conversational-core/EPIC.md)
- [E2](../E2-data-statistics/EPIC.md)
- [E3](../E3-health-care/EPIC.md)
