# Tarea técnica — Exponer la capacidad conversacional de perfil

## Resumen

Crear el caso de uso y la tool tipada que permiten responder preguntas soportadas sobre el perfil normalizado.

## Justificación

El modelo necesita una capacidad estrecha que devuelva únicamente datos autorizados y estructurados, sin conocer Firestore.

## Alcance

Incluido:
- 1. Definir la entrada cerrada de la tool sin `uid` ni rutas de Firebase.
- 2. Implementar el caso de uso que obtiene el perfil dentro del principal autenticado.
- 3. Proyectar solo los campos requeridos por la consulta.
- 4. Representar documento ausente, campo ausente y catálogo desconocido como resultados tipados.
- 5. Registrar la tool en el orquestador y proporcionar grounding para la respuesta.
- 6. Añadir casos del catálogo en español y en los idiomas finalmente aprobados.

Excluido:
- Escritura o corrección del perfil.
- Exposición del documento completo al modelo.

## Criterios de aceptación

- La tool responde solo con el perfil del principal autenticado.
- La salida diferencia dato ausente de error de infraestructura.
- La respuesta final no añade hechos no presentes en el resultado.
- Todos los casos de perfil del catálogo tienen pruebas automatizadas.

## Riesgo de no realizarla

El modelo podría recibir documentos excesivos o interpretar por sí mismo datos heredados ambiguos.

## Pruebas

- Unitarias:
  - Caso de uso, proyección y resultados ausentes.
- Integración:
  - Orquestador, tool y repositorio fake/emulado.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-08 y TASK-10 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿La API devuelve valores localizados o códigos canónicos?
  - Respuesta (Supuesto): El dominio conserva códigos canónicos y la capa de respuesta localiza según contrato.
  - Fuente de verdad: Decisión de localización pendiente.
  - Alineación: E4.

## Enlaces

- Épica/ticket relacionado: [US-04](US-04-query-dog-profile.md)
