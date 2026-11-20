# Tarea técnica — Instrumentar la API y el proveedor de IA

## Trazabilidad en Milano

- Código: `FD2E9F`.
- Story Points: 5.

## Resumen

Emitir los eventos definidos desde los límites de aplicación y recoger metadatos operativos del proveedor sin bloquear el flujo principal.

## Justificación

La observabilidad debe representar el resultado real de las operaciones y el consumo del proveedor sin duplicar eventos ni incluir payloads sensibles.

## Alcance

Incluido:
1. Crear un puerto de telemetría y un adaptador Firestore para `chatbotTelemetryEvents`.
2. Instrumentar autenticación, orquestación, tools, propuestas, confirmaciones, cuotas y errores.
3. Capturar latencia, resultado, capacidad, modelo y unidades de uso disponibles.
4. Emitir eventos terminales una sola vez incluso ante reintentos internos.
5. Aplicar redacción central y listas permitidas de propiedades.
6. Definir comportamiento no bloqueante y diagnóstico si la telemetría falla.
7. Usar marca temporal de servidor, identificador de evento e idempotencia para que los reintentos no creen dobles conteos.

Excluido:
- Agregación y endpoints de consulta.
- Registros de instrucciones o respuestas del modelo para depuración ordinaria.

## Criterios de aceptación

- Los flujos principales emiten un evento terminal con esquema válido.
- Los reintentos del proveedor no inflan conversaciones o mensajes finales.
- La caída de telemetría no provoca duplicación de escrituras de dominio.
- Tests automáticos demuestran ausencia de campos sensibles.

## Riesgo de no realizarla

No existiría evidencia fiable para operar, evaluar errores o estimar el consumo del proveedor.

## Pruebas

- Unitarias:
  - Redacción, deduplicación y mapeo provider-neutral.
- Integración:
  - Emisión a Firestore, fallo controlado y flujo completo con un doble de prueba.
- La funcionalidad existente no debe verse afectada (regresión).
