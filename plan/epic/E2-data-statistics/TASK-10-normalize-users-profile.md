# Tarea técnica — Normalizar el perfil desde Users

## Resumen

Implementar el repositorio autorizado de `Users` y la traducción del documento heredado a un modelo canónico de perfil.

## Justificación

El documento mezcla dueño, perro y estado, usa fechas textuales y catálogos numéricos, y contiene campos fuera del alcance o no confiables.

## Alcance

Incluido:
- 1. Definir el modelo canónico mínimo de perfil requerido por el catálogo.
- 2. Leer exclusivamente `Users/{uid}` usando el `uid` autenticado.
- 3. Parsear fecha de nacimiento con reglas explícitas y errores tipados.
- 4. Traducir raza, sexo, sociabilidad y energía con catálogos verificados.
- 5. Resolver variantes de foto solo si una capacidad las necesita.
- 6. Excluir premium, amigos, ubicación y paseo en curso del modelo conversacional.
- 7. Registrar diagnósticos sanitizados para datos inválidos.

Excluido:
- Mutaciones del documento `Users`.
- Inferencia de valores desconocidos por el modelo.

## Criterios de aceptación

- El repositorio no acepta un `uid` libre procedente del payload o del modelo.
- Fixtures representativos de iOS y Android producen el mismo modelo canónico cuando son equivalentes.
- Valores desconocidos permanecen ausentes o explícitamente no soportados.
- Los campos fuera de alcance no se envían al modelo.

## Riesgo de no realizarla

El chatbot podría responder con catálogos incorrectos, filtrar datos innecesarios o confiar en estado client-writable.

## Pruebas

- Unitarias:
  - Fechas, catálogos, variantes y campos inválidos.
- Integración:
  - Lectura aislada de `Users/{uid}` con emulador.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-02 y TASK-04 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué campos exactos necesita cada consulta de perfil?
  - Respuesta (Supuesto): Solo los relacionados en el catálogo validado.
  - Fuente de verdad: TASK-01.
  - Alineación: TASK-11.

## Enlaces

- Épica/ticket relacionado: [US-04](US-04-query-dog-profile.md)
