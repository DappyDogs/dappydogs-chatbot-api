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

## Riesgos y dependencias

- App Check requiere coordinación y activación en ambas aplicaciones — (Impacto: alto)
- El proveedor y el runtime cloud están pendientes de selección — (Impacto: alto)
- El estado premium actual no es una fuente de autorización confiable — (Impacto: medio)

## Hitos (opcional)

- Demo de primera consulta autenticada de perfil — 27/11/2026

## Correspondencia de entrega

- Código de Milano: `FD2DF8`.
- Estado de Milano verificado el 19 de noviembre de 2026: `todo`.
- Asignación de Milano: Sprint 1, con objetivo de demo el 27 de noviembre de 2026.
- La consulta de perfil incluida en la demo requiere que estén disponibles la adaptación de lectura de `Users` y la capacidad conversacional de perfil.
