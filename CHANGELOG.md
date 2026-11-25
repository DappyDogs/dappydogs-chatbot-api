# Registro de cambios

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto sigue el [versionado semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido

- Fundaciones ejecutables del servicio Python con configuración tipada, endpoints de salud, pruebas automatizadas, formato, lint y comprobaciones estáticas de tipos.
- Frontera de verificación de Firebase Auth y App Check con identidad derivada en el servidor, validación estricta de cabeceras, fallos saneados y pruebas de seguridad.
- Integración continua mediante GitHub Actions para comprobar formato, lint, tipos estáticos y pruebas en cada `push` y `pull request`.
- Contrato HTTP versionado con correlación generada por el servidor, logs estructurados y saneados, estructuras de error estables, límites de tamaño del cuerpo y timeouts de petición.
- Modelo canónico y fuentes de solo lectura para perfiles de `Users`, con aislamiento por identidad autenticada, normalización defensiva y fixtures anonimizados.
- Orquestador conversacional neutral al proveedor, contexto temporal acotado, registro cerrado y validado de tools y adaptador configurable, implementado inicialmente con Ollama.
- Capacidades `get_registered_pets` y `get_dog_profile` aisladas por principal autenticado, directorio `0..N` con recuento y nombres disponibles, selección de mascota por nombre, proyección mínima de atributos, conservación de códigos numéricos y ejecutor conversacional sobre las fuentes configuradas, compatible con la serialización de argumentos de Ollama.
- Respuestas sociales deterministas para saludos, agradecimientos y despedidas completas, sin consultar el modelo ni la fuente de perfiles.
- Catálogo general de consultas conversacionales con intenciones disponibles, variaciones representativas y capacidades planificadas.

## [0.1.0] - 2026-10-27

### Añadido

- Fundaciones iniciales del repositorio para la API del chatbot de IA de Dappy Dogs.
- Presentación pública del proyecto, esqueleto de comandos de desarrollo y exclusiones del repositorio orientadas a Python.
