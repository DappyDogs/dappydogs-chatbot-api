# Épica — E1 · Fundaciones y núcleo conversacional

## Objetivo de negocio

**COMO** usuario autenticado de Dappy Dogs
**NECESITO** comunicarme con un chatbot seguro y disponible desde la aplicación
**PARA** acceder mediante lenguaje natural a capacidades controladas sin exponer mis datos ni credenciales

## Contexto y justificación

No existe un backend general ni un servicio de orquestación. La API debe crear la frontera segura entre las aplicaciones, Firebase y el proveedor de IA, con autenticación, App Check, tools cerradas, límites de uso y seguridad veterinaria.

## Valor esperado / métricas de éxito

- El 100 % de endpoints protegidos rechaza Firebase Auth o App Check inválidos.
- Ninguna petición del modelo puede ejecutar una tool no declarada o argumentos fuera de contrato.
- Las consultas veterinarias prohibidas reciben una respuesta segura determinista.
- El servicio puede desplegarse y diagnosticarse sin exponer secretos ni contenido sensible.

## Alcance

Incluido:
- Fundaciones Python y contrato HTTP.
- Firebase Auth, App Check, errores, correlación y observabilidad base.
- Abstracción y selección del proveedor de IA.
- Orquestación conversacional, tools, contexto mínimo, seguridad y cuotas.
- Despliegue en el entorno de desarrollo de Google Cloud.

Excluido:
- Consultas completas de actividad y salud, desarrolladas en E2 y E3.
- Interfaz móvil.
- Validación server-side de compras, salvo ampliación expresa.

## Historias de usuario incluidas

- [US-02 — Acceder de forma segura a la API conversacional](US-02-secure-api-access.md)
- [US-03 — Mantener una conversación controlada con el modelo](US-03-controlled-conversation.md)

## Riesgos y dependencias

- App Check requiere coordinación y activación en ambas aplicaciones — (Impacto: alto)
- El proveedor y el runtime cloud están pendientes de selección — (Impacto: alto)
- El estado premium actual no es una fuente de autorización confiable — (Impacto: medio)

## Hitos (opcional)

- Demo de primera consulta autenticada de perfil — 27/11/2026

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué runtime de Google Cloud satisface streaming, timeouts, escalado y región?
  - Respuesta (Supuesto): Se desplegará en el proyecto cloud existente y en región UE compatible; el producto concreto está pendiente.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-03 y TASK-07.
- ¿La API usa respuesta completa o streaming?
  - Respuesta (Supuesto): No está decidido y debe cerrarse con los equipos móviles.
  - Fuente de verdad: Contrato de integración móvil pendiente.
  - Alineación: US-02 y E4.

## Enlaces

- [Roadmap técnico](../../ROADMAP.md)
- [E0 — Discovery](../E0-discovery/EPIC.md)
