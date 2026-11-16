# Historia de usuario — Instrumentar el uso seguro de la API

## Objetivo

**COMO** equipo operador del chatbot
**NECESITO** eventos server-side coherentes y sanitizados
**PARA** observar uso, errores, seguridad y consumo sin almacenar contenido sensible

## Contexto

El discovery solicita métricas desde el primer día. La API debe definir eventos estables para sus propias capacidades y evitar mensajes, prompts, identificadores personales de alta cardinalidad y contenido de salud.

## Alcance

Incluido:
- Taxonomía y schema de eventos.
- Instrumentación de peticiones, capacidades, confirmaciones, fallos y seguridad.
- Metadatos de consumo del proveedor.
- Redacción y pruebas de privacidad.

Excluido:
- Eventos de apertura o interacción exclusivamente móviles.
- Almacenamiento de conversaciones completas.

## Criterios de aceptación

- **AC.01.** Caso: capacidad ejecutada
  Dada una petición autenticada;
  Cuando finaliza con éxito o error controlado;
  Entonces se emite un evento con categoría, duración y resultado sin contenido sensible.
- **AC.02.** Caso: consumo del proveedor
  Dada una respuesta con metadatos de uso disponibles;
  Cuando se registra telemetría;
  Entonces se conservan cantidades operativas sin prompt, respuesta ni identidad personal.
- **AC.03.** Caso: redacción
  Dado un error que contiene datos sensibles;
  Cuando se genera log o evento;
  Entonces el contenido queda excluido o sanitizado conforme al contrato.

## Casos límite / fallos

- Backend de telemetría indisponible, eventos duplicados y cardinalidad no acotada.

## Pruebas

- Unitarias:
  - Schema, redacción y dimensiones permitidas.
- Integración:
  - Emisión no bloqueante al backend seleccionado.
- E2E:
  - Trazabilidad de una conversación sin contenido sensible.
- Visuales:
  - No aplica.

## Dependencias

- E1 y política de privacidad — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Firestore, Analytics u otra plataforma es la autoridad de eventos server-side?
  - Respuesta (Supuesto): El discovery menciona Firestore y Analytics; debe definirse una autoridad y evitar duplicación inconsistente.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-20 y TASK-21.

## Enlaces

- Épica: [E5](EPIC.md)
- Tareas: [TASK-20](TASK-20-define-telemetry-contract.md), [TASK-21](TASK-21-instrument-service-provider.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Backend y retención pendientes.
