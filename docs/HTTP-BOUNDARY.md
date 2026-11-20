# Frontera HTTP, errores y observabilidad

## Propósito

Este documento define el contrato transversal de transporte de la API de Dappy Dogs. Su objetivo es que todas las capacidades funcionales compartan versionado, límites, errores públicos, correlación y registros operativos sin exponer datos sensibles.

## Versionado y rutas operativas

Las capacidades funcionales se publican bajo el prefijo `/api/v1`, definido por `API_V1_PREFIX`. Los endpoints `/health/live` y `/health/ready` quedan fuera del prefijo porque pertenecen al plano operativo del despliegue y no al contrato funcional consumido por las aplicaciones.

La documentación interactiva permanece disponible en entornos locales y de desarrollo, y se deshabilita en producción.

## Identificador de petición

La API genera un identificador aleatorio para cada petición y lo devuelve mediante la cabecera `X-Request-ID`. El mismo valor aparece en el envelope de error y en los eventos operativos asociados a la petición.

Los valores de `X-Request-ID` enviados por el cliente se ignoran. Esta decisión impide que información personal o contenido controlado por terceros se incorpore al contexto de correlación y a los logs.

## Contrato de error

Todas las respuestas de error utilizan esta estructura cerrada:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request is invalid.",
    "request_id": "6fb741f7243446b0879fc4bb68ca7c93"
  }
}
```

Los mensajes públicos son estables y no contienen excepciones, trazas, tokens, prompts ni valores de entrada. Los códigos implementados actualmente son:

| Código | Estado HTTP | Uso |
|---|---:|---|
| `authentication_required` | 401 | Faltan evidencias de autenticación. |
| `invalid_authentication` | 401 | Firebase Auth o App Check no son válidos. |
| `authentication_unavailable` | 503 | La autenticación no está configurada. |
| `invalid_request` | 400 o 422 | Cabeceras de transporte o entrada funcional inválidas. |
| `not_found` | 404 | La ruta solicitada no existe. |
| `http_error` | Según el error | Otro rechazo HTTP controlado. |
| `request_too_large` | 413 | El cuerpo supera el límite configurado. |
| `request_timeout` | 504 | La petición supera el tiempo máximo. |
| `internal_error` | 500 | Fallo interno inesperado y saneado. |

Las respuestas `401` conservan `WWW-Authenticate: Bearer`. Las respuestas que requieren informar métodos admitidos conservan únicamente la cabecera segura `Allow`.

## Límites y cancelación

La configuración utiliza variables con prefijo `DAPPYDOGS_`:

| Variable | Valor predeterminado | Restricción |
|---|---:|---|
| `DAPPYDOGS_MAX_REQUEST_BODY_BYTES` | 1.048.576 bytes | Entero positivo. |
| `DAPPYDOGS_REQUEST_TIMEOUT_SECONDS` | 30 segundos | Número finito y positivo. |

El tamaño se comprueba mediante `Content-Length` y durante la lectura real del stream. Valores ambiguos, negativos o mal formados se rechazan. Esto evita depender de que el cliente declare correctamente el tamaño.

Cuando se alcanza el timeout, la tarea del endpoint se cancela antes de devolver `504`. Si la desconexión del cliente cancela la petición, la cancelación se propaga al servidor y no se transforma en un error interno.

## Logs estructurados y saneamiento

Los eventos HTTP se serializan como JSON y solo incluyen campos permitidos:

- Nombre del evento y nivel.
- Identificador de petición generado por el servidor.
- Método HTTP.
- Plantilla de ruta resuelta, nunca la query string.
- Estado HTTP y duración.
- Tipo de excepción, sin su mensaje ni su traza, cuando ocurre un fallo inesperado.

No se registran cuerpos, cabeceras, tokens, prompts, parámetros de consulta, identidades de usuario ni detalles de excepciones. La identidad autenticada tampoco forma parte del identificador de correlación.

## CORS

No se habilita CORS por defecto. El consumidor previsto es una aplicación móvil nativa, por lo que el transporte actual no lo necesita. Si se incorpora un cliente web, deberán definirse orígenes explícitos por entorno; no se permitirá un origen global junto con credenciales.

## Evidencia automatizada

Las pruebas cubren:

- Correlación en respuestas correctas y errores.
- Rechazo de cuerpos declarados y transmitidos por encima del límite.
- Rechazo de `Content-Length` inválido.
- Cancelación por timeout.
- Errores de validación, rutas inexistentes y fallos inesperados.
- Ausencia de tokens, prompts y trazas en respuestas y logs.
- Serialización JSON basada en una lista cerrada de campos.

