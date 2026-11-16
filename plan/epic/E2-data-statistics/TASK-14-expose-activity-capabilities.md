# Tarea técnica — Exponer tools de paseos y estadísticas

## Resumen

Integrar consultas de rutas y cálculos deterministas en tools cerradas y respuestas fundamentadas del orquestador.

## Justificación

El modelo debe seleccionar capacidades, no recibir el historial completo ni calcular cifras por su cuenta.

## Alcance

Incluido:
- 1. Definir tools para paseos por periodo, resumen y comparativas básicas.
- 2. Validar periodos, granularidad y límites antes de consultar Firestore.
- 3. Encadenar repositorio y servicios de cálculo sin exponer rutas crudas al modelo.
- 4. Producir resultados estructurados con unidades y evidencia de periodo.
- 5. Gestionar ausencia de actividad, petición ambigua y capacidad fuera de alcance.
- 6. Añadir al banco automatizado todos los casos de actividad del catálogo.

Excluido:
- Consultas geográficas o de otros usuarios.
- Comparativas no aprobadas.

## Criterios de aceptación

- Los argumentos de periodo inválidos se rechazan antes del acceso a datos.
- La respuesta usa exclusivamente cifras del servicio determinista.
- El modelo no recibe documentos de ruta ni coordenadas serializadas.
- Los casos del catálogo coinciden con resultados calculados independientemente.

## Riesgo de no realizarla

La integración podría filtrar datos excesivos o permitir que el modelo altere cifras correctas.

## Pruebas

- Unitarias:
  - Validación y proyección de resultados de tools.
- Integración:
  - Orquestador, tools, repositorio y cálculo.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-08, TASK-12 y TASK-13 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué granularidad máxima puede solicitar una conversación?
  - Respuesta (Supuesto): Solo periodos soportados por el catálogo y limitados server-side.
  - Fuente de verdad: TASK-01.
  - Alineación: TASK-09.

## Enlaces

- Épica/ticket relacionado: [US-05](US-05-query-activity-statistics.md)
