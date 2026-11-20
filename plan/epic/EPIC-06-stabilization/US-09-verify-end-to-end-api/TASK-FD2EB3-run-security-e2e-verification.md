# Tarea técnica — Ejecutar la verificación de seguridad, resiliencia y extremo a extremo

## Trazabilidad en Milano

- Código: `FD2EB3`.
- Story Points: 8.

## Resumen

Validar el servicio completo en un entorno aislado con usuarios cruzados, concurrencia, fallos externos y los flujos principales del catálogo.

## Justificación

Las pruebas unitarias no demuestran por sí solas aislamiento real, reglas de Firestore, App Check, transacciones ni comportamiento ante fallos de red.

## Alcance

Incluido:
1. Preparar usuarios, tokens, datos y secretos aislados para E2E.
2. Verificar Auth, App Check, acceso cruzado y rutas forjadas.
3. Ejecutar perfil, actividad, salud, edición y confirmación de extremo a extremo.
4. Probar reintentos, concurrencia, operación expirada y confirmación duplicada.
5. Simular timeout e indisponibilidad del proveedor, Firestore y telemetría.
6. Probar prompt injection, tools desconocidas y límites veterinarios.
7. Verificar logs, métricas y errores en busca de información sensible.
8. Consolidar hallazgos, severidad, correcciones y nueva ejecución.
9. Verificar que los flujos de perfil y actividad solo leen colecciones heredadas y que ninguna ruta de la API puede corregirlas o mutarlas.
10. Verificar que las únicas escrituras funcionales previstas se limitan a las nuevas estructuras de salud, operaciones pendientes y telemetría autorizada.

Excluido:
- Pruebas sobre producción o usuarios reales.
- Seguridad general de las apps fuera del contrato API.
- Limpieza o migración de datos históricos como parte de la estabilización.

## Criterios de aceptación

- No existe acceso cruzado ni escritura sin confirmación en los escenarios ejecutados.
- Los fallos externos producen estados controlados y no duplican efectos.
- Las pruebas de inyección no amplían tools, datos o ámbito.
- No quedan hallazgos críticos o altos atribuibles a la API sin resolver.

## Riesgo de no realizarla

Defectos de integración podrían comprometer datos o impedir la operación estable tras la entrega.

## Pruebas

- Unitarias:
  - Suite completa como prerrequisito.
- Integración:
  - Firebase, proveedor fake y fallos controlados.
- La funcionalidad existente no debe verse afectada (regresión).
