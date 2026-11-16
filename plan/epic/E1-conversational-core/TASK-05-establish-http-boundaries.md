# Tarea técnica — Establecer límites HTTP, errores y observabilidad base

## Resumen

Definir el contrato transversal de transporte para versionado, validación, errores, correlación, límites, timeouts y logs sanitizados.

## Justificación

Sin una frontera HTTP uniforme, cada capacidad resolvería de forma distinta seguridad, errores y diagnóstico, aumentando el riesgo de filtraciones y contratos móviles inestables.

## Alcance

Incluido:
- 1. Versionar rutas bajo un prefijo acordado y definir modelos cerrados de petición/respuesta.
- 2. Diseñar un envelope de error estable con códigos públicos y correlación.
- 3. Implementar request ID, logs JSON, redacción y propagación de contexto.
- 4. Aplicar límites de tamaño, timeouts y manejo de cancelación.
- 5. Definir CORS o restricciones equivalentes solo si el transporte lo requiere.
- 6. Separar errores de validación, autenticación, dominio, proveedor e infraestructura.

Excluido:
- Contratos funcionales concretos de E2 y E3.
- Dashboard de métricas.

## Criterios de aceptación

- Todas las respuestas de error siguen un contrato estable y sanitizado.
- Cada petición tiene un identificador correlacionable sin incluir identidad personal.
- Entradas sobredimensionadas o inválidas se rechazan antes de alcanzar el modelo.
- Los tests verifican que prompts, tokens y trazas no aparecen en errores o logs.

## Riesgo de no realizarla

Los clientes dependerían de errores inconsistentes y el servicio podría filtrar información sensible o aceptar abuso básico.

## Pruebas

- Unitarias:
  - Mapeo de errores y redacción.
- Integración:
  - Middleware, límites, timeouts y correlación HTTP.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-03 y contrato móvil preliminar — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿La respuesta conversacional necesita streaming?
  - Respuesta (Supuesto): Pendiente; el diseño HTTP no debe cerrarlo accidentalmente.
  - Fuente de verdad: Contrato móvil pendiente.
  - Alineación: E4.

## Enlaces

- Épica/ticket relacionado: [US-02](US-02-secure-api-access.md)
