# Épica — E4 · Integración en iOS y Android

## Objetivo de negocio

**COMO** usuario de Dappy Dogs
**NECESITO** acceder al chatbot desde las aplicaciones iOS y Android
**PARA** utilizar las capacidades de la API dentro de la experiencia habitual de la aplicación

## Contexto y justificación

El discovery asigna esta épica a los repositorios móviles: pantalla, navegación, componentes visuales, tarjeta de confirmación, estados de carga y error, localización, App Check y publicación de versiones de prueba. Este repositorio únicamente proporciona y estabiliza el contrato API consumido por esas implementaciones.

## Valor esperado / métricas de éxito

- Ambas aplicaciones consumen el mismo contrato autenticado sin lógica de negocio duplicada.
- El flujo de propuesta, edición y confirmación funciona de extremo a extremo.
- Los errores, límites y estados de seguridad de la API pueden representarse de forma estable en ambos clientes.

## Alcance

Incluido:
- Coordinación y soporte del contrato API desde las épicas E1, E2 y E3.
- Compatibilidad del contrato con Firebase Auth, App Check, reintentos y confirmación móvil.

Excluido:
- Implementación de pantallas iOS o Android en este repositorio.
- Componentes visuales, navegación y localización móvil.
- Ramas móviles, TestFlight, Google Play y publicación en tiendas.

## Paquetes externos de trabajo móvil

Estos paquetes conservan el alcance verificado de E4 en Milano sin asignar la implementación móvil a este repositorio. Deben refinarse y gestionarse en Milano y, cuando corresponda, en el repositorio móvil propietario.

1. Contrato compartido de integración móvil: envoltorios de petición y respuesta, entrega de tokens Auth y App Check, respuesta completa o streaming, tiempos de espera, reintentos, cancelación, errores estables y semántica de confirmación idempotente.
2. Integración iOS: punto de entrada y navegación, pantalla conversacional, cliente API, estados de carga y error, tarjeta editable de confirmación de salud, localización y evidencia en TestFlight.
3. Integración Android: punto de entrada y navegación, pantalla conversacional, cliente API mediante paquetes nuevos sin modificar `base.aar`, estados de carga y error, tarjeta editable de confirmación de salud, localización y evidencia en la prueba interna de Google Play.
4. Instrumentación móvil: eventos exclusivos de apertura, presentación e interacción del chatbot en Firebase Analytics conforme al catálogo compartido de E5, sin duplicar los eventos canónicos de la API.
5. Validación conjunta: ausencia de datos, cuotas, edición, confirmación y cancelación de propuestas, aplicación obligatoria de App Check, regresión y evidencia extremo a extremo en ambas plataformas.

Actualmente no existen en Milano tickets móviles verificados de bajo nivel. Estos paquetes son una propuesta de refinamiento derivada de la épica de Milano, no una afirmación de que el trabajo móvil ya esté descompuesto o asignado.

## Correspondencia de entrega

- Código de Milano: `FD2E04`.
- Estado de Milano verificado el 18 de noviembre de 2026: `backlog`.
- Sprint 2: comenzar la integración iOS únicamente cuando el contrato compartido sea suficientemente estable para su consumo.
- Sprint 3: ejecutar en paralelo la integración iOS y Android y producir evidencia de las versiones móviles de prueba.

## Riesgos y dependencias

- Contrato de streaming, reintentos y cancelación pendiente — (Impacto: alto)
- Activación coordinada de App Check — (Impacto: alto)
- Dependencia de la librería Android compilada — (Impacto: medio)

## Hitos (opcional)

- Contrato API integrado en versiones móviles de prueba — 11/12/2026
