# Historia de usuario — Consultar paseos y estadísticas de actividad

## Objetivo

**COMO** usuario autenticado
**NECESITO** consultar paseos y estadísticas por periodo
**PARA** comprender la actividad registrada de mi perro con cifras verificables

## Contexto

`Routes` contiene un documento por paseo y presenta una posible diferencia entre segundos y milisegundos. Las estadísticas deben calcularse por código con periodos, unidades y datos inválidos tratados explícitamente.

## Alcance

Incluido:
- Lectura autorizada y normalización de rutas.
- Totales, promedios, periodos semanales y mensuales.
- Comparativas básicas definidas por catálogo.
- Tools y respuestas fundamentadas.

Excluido:
- Rachas, logros, rankings, rutas geográficas y actividad en tiempo real.

## Criterios de aceptación

- **AC.01.** Caso: periodo con actividad
  Dado un periodo y rutas normalizadas del usuario;
  Cuando se solicita un resumen;
  Entonces distancia, duración, totales y promedios coinciden con un cálculo independiente.
- **AC.02.** Caso: periodo vacío
  Dado un periodo sin rutas válidas;
  Cuando se solicita actividad;
  Entonces se devuelve ausencia de actividad sin error ni cifras inventadas.
- **AC.03.** Caso: dato histórico inválido
  Dado un registro con unidad ambigua o valor malformado;
  Cuando se calcula una estadística;
  Entonces se aplica el contrato de normalización o se excluye con diagnóstico sanitizado, sin distorsión silenciosa.

## Casos límite / fallos

- Cambio de zona horaria, límites de semana/mes, rutas duplicadas, distancia cero y timestamps ambiguos.

## Pruebas

- Unitarias:
  - Normalización y cálculos de periodos.
- Integración:
  - Consultas indexadas y filtradas por `uid` sobre `Routes`.
- E2E:
  - Casos de actividad y comparación del catálogo.
- Visuales:
  - No aplica.

## Dependencias

- US-02, US-03 y evidencia de rutas de E0 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué zona horaria y primer día definen la semana?
  - Respuesta (Supuesto): Pendiente de decisión de producto.
  - Fuente de verdad: Catálogo funcional pendiente.
  - Alineación: TASK-13.

## Enlaces

- Épica: [E2](EPIC.md)
- Tareas: [TASK-12](TASK-12-normalize-routes.md), [TASK-13](TASK-13-calculate-activity-statistics.md), [TASK-14](TASK-14-expose-activity-capabilities.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Periodos y normalización pendientes.
