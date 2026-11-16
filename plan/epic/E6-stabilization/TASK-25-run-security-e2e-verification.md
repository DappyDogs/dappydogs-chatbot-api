# Tarea técnica — Ejecutar la verificación de seguridad, resiliencia y extremo a extremo

## Resumen

Validar el servicio completo en un entorno aislado con usuarios cruzados, concurrencia, fallos externos y los flujos principales del catálogo.

## Justificación

Las pruebas unitarias no demuestran por sí solas aislamiento real, reglas de Firestore, App Check, transacciones ni comportamiento ante fallos de red.

## Alcance

Incluido:
- 1. Preparar usuarios, tokens, datos y secretos aislados para E2E.
- 2. Verificar Auth, App Check, acceso cruzado y rutas forjadas.
- 3. Ejecutar perfil, actividad, salud, edición y confirmación de extremo a extremo.
- 4. Probar reintentos, concurrencia, operación expirada y confirmación duplicada.
- 5. Simular timeout e indisponibilidad del proveedor, Firestore y telemetría.
- 6. Probar prompt injection, tools desconocidas y límites veterinarios.
- 7. Verificar logs, métricas y errores en busca de información sensible.
- 8. Consolidar hallazgos, severidad, correcciones y nueva ejecución.

Excluido:
- Pruebas sobre producción o usuarios reales.
- Seguridad general de las apps fuera del contrato API.

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

## Dependencias

- TASK-24 y despliegue integrado de E1–E5 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué entorno y datos están autorizados para la prueba final?
  - Respuesta (Supuesto): Proyecto de desarrollo con datos sintéticos o anonimizados y cuentas aisladas.
  - Fuente de verdad: Decisión de entorno pendiente.
  - Alineación: TASK-02 y TASK-06.

## Enlaces

- Épica/ticket relacionado: [US-10](US-10-verify-end-to-end-api.md)
