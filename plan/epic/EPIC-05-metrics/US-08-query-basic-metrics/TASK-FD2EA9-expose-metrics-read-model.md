# Tarea técnica — Exponer el modelo de lectura de métricas

## Trazabilidad en Milano

- Código: `FD2EA9`.
- Story Points: 3.

## Resumen

Proporcionar una superficie autorizada y estable para que la vista elegida consulte los agregados básicos.

## Justificación

Los agregados operativos no deben ser públicos ni accesibles mediante la identidad ordinaria de un usuario final.

## Alcance

Incluido:
1. Implementar en la API el modelo de lectura autorizado sobre `chatbotMetricsDaily`; la vista visual puede ser una página o herramienta externa.
2. Definir principal y rol operativo confiables independientes del premium client-writable.
3. Diseñar filtros de periodo, paginación y respuesta tipada.
4. Aplicar autorización, límites, auditoría y errores sanitizados.
5. Publicar definiciones de métricas junto con el contrato de lectura.
6. Verificar que no se exponen eventos crudos ni dimensiones personales.

Excluido:
- Diseño visual del dashboard si reside fuera del repositorio.
- Administración general de usuarios.

## Criterios de aceptación

- Solo una identidad operativa autorizada accede a los agregados.
- La respuesta contiene las métricas acordadas y sus periodos, no eventos crudos.
- Los filtros inválidos y accesos no autorizados se rechazan de forma estable.
- El contrato soporta la vista elegida sin exponer contenido sensible.

## Riesgo de no realizarla

Las métricas podrían quedar inaccesibles o exponerse mediante controles de usuario inadecuados.

## Pruebas

- Unitarias:
  - Autorización, filtros y modelos de respuesta.
- Integración:
  - Acceso operativo, rechazo y consulta del almacén agregado.
- La funcionalidad existente no debe verse afectada (regresión).
