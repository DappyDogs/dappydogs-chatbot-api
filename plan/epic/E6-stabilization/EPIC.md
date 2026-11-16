# Épica — E6 · Estabilización y entrega de la API

## Objetivo de negocio

**COMO** equipo responsable de operar Dappy Dogs
**NECESITO** una API estable, verificable y documentada
**PARA** integrar y mantener el chatbot con un riesgo operativo controlado

## Contexto y justificación

La entrega requiere verificar el flujo principal de extremo a extremo, cerrar errores críticos y proporcionar documentación técnica mínima de arquitectura, despliegue, configuración y operación.

## Valor esperado / métricas de éxito

- El catálogo acordado supera las pruebas automatizadas y la verificación de extremo a extremo.
- No quedan defectos críticos abiertos en autenticación, aislamiento, confirmación o seguridad veterinaria.
- El despliegue es reproducible y dispone de runbook, configuración y observabilidad verificadas.

## Alcance

Incluido:
- Banco automatizado y pruebas integradas del catálogo.
- Verificación de seguridad, resiliencia y regresión.
- Ajuste controlado de instrucciones del modelo basado en evidencia.
- Documentación técnica y traspaso operativo de la API.

Excluido:
- Revisión de Apple o Google y publicación en tiendas.
- Corrección de hallazgos heredados fuera del alcance del chatbot.

## Historias de usuario incluidas

- [US-10 — Verificar el flujo completo de la API](US-10-verify-end-to-end-api.md)
- [US-11 — Operar y mantener la API entregada](US-11-operate-delivered-api.md)

## Riesgos y dependencias

- Dependencia de versiones móviles integradas y entorno estable — (Impacto: alto)
- Falta de datos de prueba representativos — (Impacto: alto)
- Cambios tardíos de proveedor, catálogo o contratos — (Impacto: alto)

## Hitos (opcional)

- Flujo completo disponible para integración móvil — 11/12/2026
- Entrega técnica — 18/12/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué evidencia exacta constituye el acta de verificación de la API?
  - Respuesta (Supuesto): Matriz catálogo-prueba, resultados E2E, controles de seguridad y versión desplegada identificable.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: US-10.
- ¿Quién recibe alertas y opera el servicio tras la entrega?
  - Respuesta (Supuesto): Pendiente de definir en el traspaso operativo.
  - Fuente de verdad: Modelo operativo pendiente.
  - Alineación: US-11.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E1](../E1-conversational-core/EPIC.md)
- [E2](../E2-data-statistics/EPIC.md)
- [E3](../E3-health-care/EPIC.md)
- [E5](../E5-metrics/EPIC.md)
