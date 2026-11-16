# Historia de usuario — Mantener una conversación controlada con el modelo

## Objetivo

**COMO** usuario de Dappy Dogs
**NECESITO** expresar consultas en lenguaje natural
**PARA** recibir respuestas fundamentadas mediante capacidades autorizadas y seguras

## Contexto

El modelo debe permanecer aislado de Firebase y operar únicamente mediante tools cerradas. La aplicación necesita contexto mínimo, proveedor sustituible, límites de uso y protección veterinaria determinista.

## Alcance

Incluido:
- Evaluación y adaptador del proveedor.
- Contexto conversacional acotado y tools tipadas.
- Validación de salida, fallos controlados y grounding.
- Límites veterinarios y cuotas server-side.

Excluido:
- Entrenamiento o fine-tuning de modelos.
- Tools fuera del catálogo inicial.

## Criterios de aceptación

- **AC.01.** Caso: tool válida
  Dada una consulta compatible con una capacidad declarada;
  Cuando el modelo solicita la tool con argumentos válidos;
  Entonces la API la autoriza, ejecuta y devuelve una respuesta basada en el resultado estructurado.
- **AC.02.** Caso: salida no confiable
  Dada una tool desconocida, argumentos adicionales o salida inválida;
  Cuando se valida la respuesta del modelo;
  Entonces no se ejecuta ninguna acción y se produce un resultado controlado.
- **AC.03.** Caso: consulta veterinaria prohibida
  Dada una solicitud de diagnóstico o tratamiento;
  Cuando se aplica la política de seguridad;
  Entonces se devuelve el mensaje fijo acordado sin ejecutar una tool de datos como sustituto.
- **AC.04.** Caso: límite alcanzado
  Dado un usuario que ha agotado su cuota;
  Cuando envía otro mensaje;
  Entonces la API rechaza la operación de forma estable antes de consumir al proveedor.

## Casos límite / fallos

- Prompt injection, proveedor indisponible, timeout, truncado, rechazo de seguridad y contexto excesivo.

## Pruebas

- Unitarias:
  - Registro de tools, política veterinaria, contexto y cuotas.
- Integración:
  - Contrato del adaptador de modelo con respuestas válidas e inválidas.
- E2E:
  - Primera consulta autenticada de perfil mediante una tool real del entorno de desarrollo.
- Visuales:
  - No aplica.

## Dependencias

- US-02 y catálogo de E0 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué proveedor y modelo cumplen calidad, tools, privacidad y latencia?
  - Respuesta (Supuesto): Se decidirá mediante un banco de pruebas sobre el catálogo validado.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-07.
- ¿Qué límites se aplican por usuario y plan?
  - Respuesta (Supuesto): Pendiente de decisión; el estado premium actual no es confiable.
  - Fuente de verdad: Hallazgo S4 del discovery.
  - Alineación: TASK-09.

## Enlaces

- Épica: [E1](EPIC.md)
- Tareas: [TASK-07](TASK-07-evaluate-model-provider.md), [TASK-08](TASK-08-build-conversation-orchestrator.md), [TASK-09](TASK-09-enforce-safety-quotas.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Proveedor, contexto y cuotas pendientes.
