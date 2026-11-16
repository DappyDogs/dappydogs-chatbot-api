# Tarea técnica — Instrumentar la API y el proveedor de IA

## Resumen

Emitir los eventos definidos desde los límites de aplicación y recoger metadatos operativos del proveedor sin bloquear el flujo principal.

## Justificación

La observabilidad debe representar el resultado real de las operaciones y el consumo del proveedor sin duplicar eventos ni incluir payloads sensibles.

## Alcance

Incluido:
- 1. Crear un puerto de telemetría y un adaptador para el backend elegido.
- 2. Instrumentar autenticación, orquestación, tools, propuestas, confirmaciones, cuotas y errores.
- 3. Capturar latencia, resultado, capacidad, modelo y unidades de uso disponibles.
- 4. Emitir eventos terminales una sola vez incluso ante retries internos.
- 5. Aplicar redacción central y listas permitidas de propiedades.
- 6. Definir comportamiento no bloqueante y diagnóstico si la telemetría falla.

Excluido:
- Agregación y endpoints de consulta.
- Logs de prompts o respuestas para depuración ordinaria.

## Criterios de aceptación

- Los flujos principales emiten un evento terminal con schema válido.
- Los retries del proveedor no inflan conversaciones o mensajes finales.
- La caída de telemetría no provoca duplicación de escrituras de dominio.
- Tests automáticos demuestran ausencia de campos sensibles.

## Riesgo de no realizarla

No existiría evidencia fiable para operar, evaluar errores o estimar el consumo del proveedor.

## Pruebas

- Unitarias:
  - Redacción, deduplicación y mapeo provider-neutral.
- Integración:
  - Emisión, fallo del backend y pipeline completo con fake.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-08, TASK-18 y TASK-20 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué metadata de uso garantiza el proveedor seleccionado?
  - Respuesta (Supuesto): Se documentará en TASK-07 y se mapeará a campos opcionales.
  - Fuente de verdad: Resultado de evaluación del proveedor.
  - Alineación: TASK-22.

## Enlaces

- Épica/ticket relacionado: [US-08](US-08-instrument-api-usage.md)
