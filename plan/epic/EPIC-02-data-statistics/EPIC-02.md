# Épica — E2 · Consulta de datos y estadísticas

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** consultar el perfil de mi perro y su actividad mediante lenguaje natural
**PARA** obtener respuestas correctas sin localizar manualmente la información en la aplicación

## Contexto y justificación

La exportación de solo lectura confirma que la base heredada no tiene un esquema uniforme. `Users` presenta 87 variantes superiores y mezcla cuenta, propietario, perro, dispositivo, suscripción, localización, relaciones y paseo en curso. `Routes` es más estable, con dos variantes, pero combina enteros y decimales, coordenadas serializadas, un `id` opcional no canónico y valores atípicos. La API debe describir todas las variaciones observadas y traducir en memoria únicamente los campos necesarios para el chatbot, sin modificar Firestore.

## Valor esperado / métricas de éxito

- Las consultas del catálogo devuelven cifras coincidentes con cálculos independientes sobre datos controlados.
- Los registros inválidos o incompletos no distorsionan silenciosamente las estadísticas.
- Ninguna respuesta incluye datos de otra cuenta.
- Todas las variantes observadas de las colecciones heredadas quedan representadas mediante contratos de lectura y fixtures, aunque una colección no alimente capacidades del chatbot.

## Alcance

Incluido:
- Contratos de lectura y datos de prueba para todas las variaciones observadas de `Users` y `Routes` que afecten al perfil o la actividad.
- Modelos canónicos y adaptación de solo lectura de `Users` y `Routes`.
- Consultas de perfil y paseos por periodo.
- Totales, promedios, actividad semanal y mensual y comparativas básicas.
- Tools estructuradas y respuestas fundamentadas.

Excluido:
- Paseos en curso, ubicación, rachas, logros y clasificaciones.
- Comparativas avanzadas, tendencias y mensajes motivacionales.
- Limpieza, reparación, backfill, migración, renombrado o reestructuración de colecciones y documentos existentes.
- Capacidades sociales, mensajería, notificaciones o modificación de datos heredados.
- Catalogación exhaustiva de colecciones que no participan en las capacidades contratadas.

## Riesgos y dependencias

- Semántica exacta de `Routes.time` pendiente de confirmar con ambos productores móviles; la exportación observada tiene escala de segundos — (Impacto: medio)
- Catálogos numéricos canónicos no disponibles todavía — (Impacto: medio)
- Datos históricos heterogéneos o incompletos — (Impacto: medio)
- Semántica de catálogos y formatos de `Users` y `Routes` dependiente de las aplicaciones móviles — (Impacto: alto)

## Hitos (opcional)

- Catálogo de consultas y estadísticas operativo — 04/12/2026

## Correspondencia de entrega

- Código de Milano: `FD2DFC`.
- Estado de Milano verificado el 18 de noviembre de 2026: `backlog`.
- Asignación de Milano: Sprint 1; el plan técnico distribuye el primer perfil en Sprint 1 y la actividad restante en el carril backend de Sprint 2.
- El banco automatizado comprometido por Milano se desarrolla progresivamente y no se aplaza por completo hasta la estabilización final.
