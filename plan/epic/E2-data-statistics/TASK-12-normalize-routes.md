# Tarea técnica — Normalizar y consultar Routes por periodo

## Resumen

Implementar el repositorio autorizado de rutas y su traducción a registros canónicos de actividad.

## Justificación

Las rutas pueden diferir en unidades de timestamp y contener valores ausentes o inválidos que no deben distorsionar cálculos.

## Alcance

Incluido:
- 1. Definir el modelo canónico mínimo de paseo con instante final, duración y distancia.
- 2. Diseñar consultas filtradas por usuario y periodo compatibles con índices verificados.
- 3. Detectar y normalizar unidades de timestamp únicamente con reglas respaldadas por evidencia.
- 4. Normalizar segundos y metros sin usar el recorrido serializado.
- 5. Definir política para rutas sin distancia, duplicadas o malformadas.
- 6. Aplicar paginación y límites para historiales grandes.
- 7. Emitir diagnósticos sanitizados de exclusión de registros.

Excluido:
- Deserialización de coordenadas y actividad en curso.
- Reparación de documentos históricos.

## Criterios de aceptación

- Solo se consultan rutas del `uid` autenticado y dentro del periodo autorizado.
- Los fixtures de segundos y milisegundos se normalizan según el contrato verificado.
- Los registros inválidos no se convierten silenciosamente en cero.
- La consulta usa índices y paginación definidos, sin escaneo global.

## Riesgo de no realizarla

Las cifras podrían ser incorrectas y las consultas degradarse o cruzar ámbitos de usuario.

## Pruebas

- Unitarias:
  - Unidades, validación, duplicados y límites de periodo.
- Integración:
  - Consultas indexadas y aisladas con emulador.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-02 y TASK-04 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Cómo se distinguen de forma inequívoca segundos y milisegundos?
  - Respuesta (Supuesto): Mediante contrato por campo/origen confirmado con datos reales, no por heurística de magnitud aislada.
  - Fuente de verdad: Auditoría TASK-02.
  - Alineación: TASK-13.

## Enlaces

- Épica/ticket relacionado: [US-05](US-05-query-activity-statistics.md)
