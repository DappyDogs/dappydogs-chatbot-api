# Historia de usuario — Consultar métricas básicas del chatbot

## Objetivo

**COMO** responsable del producto Dappy Dogs
**NECESITO** consultar métricas básicas del chatbot
**PARA** conocer adopción, distribución de uso, errores y consumo estimado

## Contexto

La vista debe mostrar usuarios activos, conversaciones, mensajes, uso por tipo, registros creados, errores y consumo estimado. Todavía no se ha decidido si la API servirá la vista o únicamente los agregados.

## Alcance

Incluido:
- Definición de agregados y periodos.
- Proceso de agregación server-side asignado a la API.
- Superficie autenticada de consulta si se decide servirla desde este repositorio.

Excluido:
- Analítica avanzada y contenido de conversaciones.
- Diseño de un dashboard externo no alojado por la API.

## Criterios de aceptación

- **AC.01.** Caso: periodo con actividad
  Dado un usuario autorizado de operación y un periodo válido;
  Cuando consulta las métricas;
  Entonces obtiene los agregados acordados con definiciones estables y sin datos personales innecesarios.
- **AC.02.** Caso: acceso no autorizado
  Dada una identidad sin rol operativo válido;
  Cuando solicita métricas;
  Entonces la API rechaza el acceso sin revelar agregados.
- **AC.03.** Caso: datos incompletos
  Dado un proveedor sin alguna métrica de consumo;
  Cuando se calcula la vista;
  Entonces se declara la ausencia sin estimaciones inventadas.

## Casos límite / fallos

- Periodos vacíos, eventos tardíos, duplicados, cambio de proveedor y zonas horarias.

## Pruebas

- Unitarias:
  - Agregaciones, deduplicación y periodos.
- Integración:
  - Autorización y consulta sobre el almacén acordado.
- E2E:
  - Vista básica con datos controlados.
- Visuales:
  - No aplica si este repositorio solo ofrece datos.

## Dependencias

- US-08 y decisión sobre formato de la vista — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué identidad y rol autorizan el acceso a métricas?
  - Respuesta (Supuesto): Debe existir un control server-side independiente del estado premium de usuarios finales.
  - Fuente de verdad: Decisión de operación pendiente.
  - Alineación: TASK-23.

## Enlaces

- Épica: [E5](EPIC.md)
- Tareas: [TASK-22](TASK-22-build-metrics-aggregation.md), [TASK-23](TASK-23-expose-metrics-read-model.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Vista y autorización pendientes.
