# Registro de cambios

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto sigue el [versionado semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido

- Fundaciones ejecutables del servicio Python con configuración tipada, endpoints de salud, pruebas automatizadas, formato, lint y comprobaciones estáticas de tipos.
- Frontera de verificación de Firebase Auth y App Check con identidad derivada en el servidor, validación estricta de cabeceras, fallos saneados y pruebas de seguridad.
- Integración continua mediante GitHub Actions para comprobar formato, lint, tipos estáticos y pruebas en cada `push` y `pull request`.
- Contrato HTTP versionado con correlación generada por el servidor, logs estructurados y saneados, estructuras de error estables, límites de tamaño del cuerpo y timeouts de petición.
- Modelo canónico y adaptadores de solo lectura para perfiles heredados de `Users`, con aislamiento por identidad autenticada, normalización defensiva y fixtures anonimizados.

## [0.1.0] - 2026-10-27

### Añadido

- Fundaciones iniciales del repositorio para la API del chatbot de IA de Dappy Dogs.
- Presentación pública del proyecto, esqueleto de comandos de desarrollo y exclusiones del repositorio orientadas a Python.
