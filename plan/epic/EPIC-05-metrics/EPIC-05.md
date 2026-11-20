# Épica — E5 · Instrumentación y métricas

## Objetivo de negocio

**COMO** responsable del producto Dappy Dogs
**NECESITO** observar el uso y la fiabilidad del chatbot
**PARA** evaluar adopción, detectar errores y controlar el consumo del proveedor sin acceder a contenido sensible

## Contexto y justificación

El discovery requiere eventos de apertura, mensajes, tipos de consulta, registros confirmados, errores y coste estimado. Las aplicaciones registran en Firebase Analytics los eventos exclusivos de interfaz; la API persiste en Firestore los eventos sanitizados de servidor y los metadatos de consumo del proveedor. La vista básica se alimenta de agregados del servidor sin leer conversaciones ni duplicar eventos entre propietarios.

## Valor esperado / métricas de éxito

- Los eventos del servidor cubren conversaciones, capacidades, confirmaciones, errores, seguridad y consumo del proveedor.
- Firebase Analytics cubre apertura, presentación e interacción móvil conforme al catálogo compartido.
- Ningún evento o registro contiene mensajes, instrucciones o respuestas del modelo, tokens, ubicaciones ni datos de salud.
- La vista acordada puede mostrar usuarios activos, conversaciones, mensajes, uso por tipo, registros, errores y consumo estimado.

## Alcance

Incluido:
- Taxonomía y emisión de eventos del servidor.
- Métricas de fiabilidad, seguridad y consumo del proveedor.
- Agregación y superficie de consulta asignadas a la API.
- Nuevas colecciones `chatbotTelemetryEvents` y `chatbotMetricsDaily`, aisladas de las colecciones heredadas.

Excluido:
- Eventos de interfaz exclusivos de iOS y Android.
- Analítica avanzada, cohortes, tendencias o motivación.

## Límite transversal de analítica

- La API es responsable de eventos sanitizados de petición, capacidad, confirmación, seguridad, fallo y consumo del proveedor.
- La API escribe esos eventos en `chatbotTelemetryEvents` y genera agregados temporales en `chatbotMetricsDaily` para la vista básica.
- Las aplicaciones móviles son responsables de Firebase Analytics para eventos exclusivos de interfaz, como entrada al chatbot, presentación de pantalla y estados de interacción del cliente.
- Un catálogo compartido alinea nombres y significado de negocio, pero cada evento tiene un único productor responsable para evitar dobles conteos.
- Ningún origen puede incluir mensajes, instrucciones o respuestas del modelo, tokens, ubicaciones ni contenido de salud.
- Milano conserva como entregable la vista básica de métricas. Su superficie visual, retención y política de acceso deben cerrarse antes de finalizar el modelo de lectura, pero el modelo de datos y la API de lectura pertenecen a este repositorio.

## Correspondencia de entrega

- Código de Milano: `FD2E08`.
- Estado de Milano verificado el 18 de noviembre de 2026: `backlog`.
- Sprint 3: implementar en este repositorio el carril del servidor mientras los equipos móviles implementan por separado sus fuentes de eventos.

## Riesgos y dependencias

- Formato visual de la vista aún no decidido — (Impacto: medio)
- Riesgo de alta cardinalidad o exposición de datos — (Impacto: alto)
- Metadatos de consumo distintos según proveedor — (Impacto: medio)

## Hitos (opcional)

- Vista básica accesible para validación — 18/12/2026
