# Tarea técnica — Aplicar seguridad veterinaria y límites de uso

## Resumen

Implementar políticas server-side para bloquear asesoramiento veterinario prohibido y limitar consumo por identidad antes de invocar al proveedor.

## Justificación

Las instrucciones del modelo no bastan para garantizar seguridad médica ni control de abuso. El estado premium actual tampoco puede usarse como autorización confiable.

## Alcance

Incluido:
- 1. Definir categorías permitidas, prohibidas y ambiguas con respuesta segura acordada.
- 2. Aplicar controles deterministas antes de tools y filtro de salida después del modelo.
- 3. Probar diagnóstico, tratamiento, prescripción, dosis y prompt injection.
- 4. Diseñar cuota por `uid` con contadores atómicos, periodo y zona horaria definidos.
- 5. Rechazar límites alcanzados antes de consumir al proveedor.
- 6. Emitir eventos sanitizados de seguridad y cuota.

Excluido:
- Validación server-side de compras.
- Consejos veterinarios personalizados.

## Criterios de aceptación

- Las categorías prohibidas producen la respuesta fija sin tool ni recomendación clínica.
- La política funciona con un fake de modelo que intenta devolver contenido inseguro.
- La cuota es concurrency-safe y no confía en valores enviados por el cliente.
- Si se decide acceso premium, la tarea permanece bloqueada hasta disponer de entitlement confiable.

## Riesgo de no realizarla

El sistema podría emitir recomendaciones médicas improcedentes o permitir consumo no controlado.

## Pruebas

- Unitarias:
  - Política, filtros, contador y límites de periodo.
- Integración:
  - Concurrencia de cuotas y pipeline completo de seguridad.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-01, TASK-08 y decisión de acceso — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué cuota y periodo se aplican a cada usuario?
  - Respuesta (Supuesto): Pendiente de decisión de producto y sin dependencia del premium client-writable.
  - Fuente de verdad: Catálogo y política de acceso pendientes.
  - Alineación: E5.

## Enlaces

- Épica/ticket relacionado: [US-03](US-03-controlled-conversation.md)
