# Épica — E5 · Instrumentación y métricas

## Objetivo de negocio

**COMO** responsable del producto Dappy Dogs
**NECESITO** observar el uso y la fiabilidad del chatbot
**PARA** evaluar adopción, detectar errores y controlar el consumo del proveedor sin acceder a contenido sensible

## Contexto y justificación

El discovery requiere eventos de apertura, mensajes, tipos de consulta, registros confirmados, errores y consumo estimado. Este repositorio es responsable de la instrumentación server-side y de la agregación o consulta que se le asigne; los eventos puramente móviles pertenecen a las apps.

## Valor esperado / métricas de éxito

- Los eventos server-side cubren conversaciones, capacidades, confirmaciones, errores, seguridad y consumo del proveedor.
- Ningún evento o log contiene mensajes, prompts, tokens, ubicaciones ni datos de salud.
- La vista acordada puede mostrar usuarios activos, conversaciones, mensajes, uso por tipo, registros, errores y consumo estimado.

## Alcance

Incluido:
- Taxonomía y emisión de eventos server-side.
- Métricas de fiabilidad, seguridad y consumo del proveedor.
- Agregación y superficie de consulta asignadas a la API.

Excluido:
- Eventos de interfaz exclusivos de iOS y Android.
- Analítica avanzada, cohortes, tendencias o motivación.

## Historias de usuario incluidas

- [US-08 — Instrumentar el uso seguro de la API](US-08-instrument-api-usage.md)
- [US-09 — Consultar métricas básicas del chatbot](US-09-query-basic-metrics.md)

## Riesgos y dependencias

- Formato y propietario de la vista aún no decididos — (Impacto: medio)
- Riesgo de alta cardinalidad o exposición de datos — (Impacto: alto)
- Metadatos de consumo distintos según proveedor — (Impacto: medio)

## Hitos (opcional)

- Vista básica accesible para validación — 18/12/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿La vista se sirve desde esta API, una página separada o una herramienta existente?
  - Respuesta (Supuesto): Pendiente de decisión de producto.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: US-09.
- ¿Qué retención y granularidad se autorizan para los eventos?
  - Respuesta (Supuesto): Deben definirse antes de persistir eventos en producción.
  - Fuente de verdad: Política de privacidad pendiente.
  - Alineación: US-08 y US-09.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E1 — Núcleo conversacional](../E1-conversational-core/EPIC.md)
