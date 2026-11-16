# Historia de usuario — Verificar el flujo completo de la API

## Objetivo

**COMO** responsable de aceptar el chatbot
**NECESITO** evidencia automatizada y reproducible del comportamiento de la API
**PARA** confirmar que el catálogo funciona sin errores críticos ni fugas entre cuentas

## Contexto

La aceptación requiere relacionar cada consulta y acción acordada con resultados verificables, además de probar autenticación, aislamiento, confirmaciones, seguridad veterinaria y fallos externos.

## Alcance

Incluido:
- Banco automatizado del catálogo.
- Matriz de trazabilidad entre casos, tools, datos y pruebas.
- Pruebas integradas de seguridad, resiliencia y flujos principales.
- Informe reproducible de verificación.

Excluido:
- Pruebas visuales de las aplicaciones.
- Revisión de publicación de Apple o Google.

## Criterios de aceptación

- **AC.01.** Caso: catálogo completo
  Dado el catálogo validado;
  Cuando se ejecuta el banco contra datos controlados;
  Entonces cada caso produce la capacidad y el resultado esperado o una limitación explícitamente aceptada.
- **AC.02.** Caso: aislamiento y confirmación
  Dados usuarios y operaciones cruzadas;
  Cuando se ejecutan las pruebas negativas;
  Entonces ninguna cuenta accede a otra y ninguna escritura evita la confirmación.
- **AC.03.** Caso: fallo externo
  Dada indisponibilidad simulada del proveedor o Firestore;
  Cuando se ejecuta el flujo;
  Entonces la API responde de forma controlada sin duplicar escrituras ni filtrar detalles.

## Casos límite / fallos

- Concurrencia, reintentos, timeouts, datos malformados y cambios de periodo.

## Pruebas

- Unitarias:
  - Suite completa sin regresiones.
- Integración:
  - Adaptadores, reglas, índices y transacciones.
- E2E:
  - Catálogo y flujos críticos en entorno aislado.
- Visuales:
  - No aplica en este repositorio.

## Dependencias

- E1, E2, E3 y E5 — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué casos requieren proveedor real frente a fake determinista?
  - Respuesta (Supuesto): El contrato funcional se verifica con fakes; una evaluación controlada del modelo usa el proveedor real y datos anonimizados.
  - Fuente de verdad: Estrategia de pruebas del contexto técnico.
  - Alineación: TASK-24 y TASK-25.

## Enlaces

- Épica: [E6](EPIC.md)
- Tareas: [TASK-24](TASK-24-build-catalog-test-harness.md), [TASK-25](TASK-25-run-security-e2e-verification.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Estrategia E2E pendiente.
