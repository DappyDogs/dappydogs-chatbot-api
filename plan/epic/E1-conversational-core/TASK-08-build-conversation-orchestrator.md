# Tarea técnica — Construir el orquestador conversacional y el registro de tools

## Resumen

Implementar el caso de uso que procesa un turno, mantiene contexto acotado, invoca el modelo, valida tools y compone una respuesta fundamentada.

## Justificación

La separación entre modelo y datos depende de un orquestador que controle explícitamente qué información y acciones puede utilizar el proveedor.

## Alcance

Incluido:
- 1. Definir puertos provider-neutral para mensajes, salida estructurada, uso y errores.
- 2. Diseñar contexto conversacional con propiedad, tamaño y expiración acotados.
- 3. Crear un registro versionado de tools con schemas cerrados y handlers de aplicación.
- 4. Validar nombre, argumentos, propiedades adicionales y autorización antes de ejecutar.
- 5. Separar instrucciones, contenido de usuario, datos y resultados de tools.
- 6. Gestionar aclaraciones, datos ausentes, tools múltiples permitidas y fallos del proveedor.
- 7. Construir respuestas fundamentadas sin afirmar acciones no ejecutadas.

Excluido:
- Implementación interna de las tools de E2 y E3.
- Persistencia indefinida de conversaciones.

## Criterios de aceptación

- El dominio y aplicación no importan tipos del SDK del proveedor.
- Solo se ejecutan tools registradas y argumentos completamente validados.
- La identidad nunca procede del modelo ni de argumentos de tool.
- Los fallos y outputs inválidos no ejecutan efectos y producen respuestas controladas.

## Riesgo de no realizarla

El modelo podría convertirse en una frontera de autorización o ejecutar acciones no gobernadas.

## Pruebas

- Unitarias:
  - Registro, validación, contexto y estados del orquestador.
- Integración:
  - Adaptador seleccionado mediante fake contractual y casos inválidos.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-03, TASK-05 y TASK-07 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Dónde y cuánto tiempo se conserva el contexto?
  - Respuesta (Supuesto): Solo el mínimo necesario, con TTL configurable; backend pendiente.
  - Fuente de verdad: Decisión de retención pendiente.
  - Alineación: TASK-09 y E3.

## Enlaces

- Épica/ticket relacionado: [US-03](US-03-controlled-conversation.md)
