# Tarea técnica — Producir documentación y traspaso técnico

## Resumen

Documentar la arquitectura implementada, contratos, despliegue, configuración, operación, seguridad y evidencia de verificación para el equipo receptor.

## Justificación

La API no puede mantenerse con conocimiento implícito ni con documentación que describa decisiones previstas pero no implementadas.

## Alcance

Incluido:
- 1. Documentar arquitectura, límites de confianza, flujo conversacional y confirmación.
- 2. Publicar contrato API, códigos de error, autenticación, App Check e idempotencia.
- 3. Documentar modelos canónicos, tools, healthRecords, reglas, índices y migraciones.
- 4. Documentar settings, secretos, despliegue, rollback, salud, métricas y alertas.
- 5. Consolidar matriz catálogo-pruebas y resultados de seguridad sin datos sensibles.
- 6. Preparar runbooks de diagnóstico, proveedor degradado, Firestore degradado y rotación.
- 7. Realizar sesión de traspaso y registrar preguntas abiertas y responsables.
- 8. Alinear README, changelog y versión con el estado realmente entregado.

Excluido:
- Documentación interna de iOS, Android o sistemas heredados.
- Afirmaciones sobre capacidades no verificadas.

## Criterios de aceptación

- Un operador puede desplegar, verificar, diagnosticar y revertir siguiendo la documentación.
- Los contratos documentados coinciden con código y tests de la versión entregada.
- No aparecen secretos, datos personales ni materiales locales en documentación pública.
- Las limitaciones y responsabilidades externas quedan claramente delimitadas.

## Riesgo de no realizarla

La operación dependería de conocimiento tácito y aumentaría el tiempo de recuperación y el riesgo de cambios incompatibles.

## Pruebas

- Unitarias:
  - No aplica directamente.
- Integración:
  - Recorrido de los runbooks por una persona distinta de su autor.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-25, TASK-26 y versión candidata final — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Quién acepta formalmente el traspaso técnico?
  - Respuesta (Supuesto): El responsable técnico y operativo designado por Dappy Dogs.
  - Fuente de verdad: Plan de entrega pendiente.
  - Alineación: E6.

## Enlaces

- Épica/ticket relacionado: [US-11](US-11-operate-delivered-api.md)
