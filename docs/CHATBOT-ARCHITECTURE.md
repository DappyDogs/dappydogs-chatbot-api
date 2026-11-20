# Arquitectura del chatbot de Dappy Dogs

## Estado del documento

Este documento describe la arquitectura objetivo del chatbot de Dappy Dogs. Sirve como base para diseñar el producto y sus contratos técnicos; no implica que todas las capacidades descritas estén ya implementadas.

Las decisiones sobre proveedor del modelo, alojamiento, transmisión de respuestas y contratos definitivos de datos permanecen abiertas hasta completar su validación técnica y de producto.

## 1. Principio fundamental

El modelo de lenguaje interpreta la petición del usuario y redacta una respuesta natural. La API de Dappy Dogs conserva el control de los datos, la autorización, las reglas de negocio y cualquier operación persistente.

```text
Aplicación móvil
  → API de Dappy Dogs
    → modelo de lenguaje
      → solicitud de una capacidad permitida
    → API valida, consulta o prepara una operación
      → resultado estructurado
    → modelo redacta la respuesta
  → aplicación móvil
```

El modelo no debe acceder directamente a Firebase ni recibir credenciales de infraestructura.

## 2. Acceso a datos mediante capacidades cerradas

La API ofrecerá al modelo un catálogo explícito de capacidades. Cada capacidad tendrá un propósito concreto, parámetros validados y una respuesta estructurada.

Ejemplos candidatos:

- Consultar el resumen de actividad reciente del perro.
- Comparar paseos de dos periodos.
- Recuperar información de perfil necesaria para personalizar una respuesta.
- Preparar una propuesta de actualización que requiera confirmación.

No se expondrán herramientas genéricas para ejecutar consultas arbitrarias, escribir documentos libres o elegir colecciones y campos dinámicamente.

El usuario efectivo se obtendrá en el servidor a partir del token de Firebase Authentication. Un identificador enviado dentro del mensaje o de los argumentos del modelo nunca sustituirá esa identidad autenticada.

## 3. Autenticación y autorización

La frontera de autenticación ya implementada aplica el siguiente flujo a cualquier endpoint protegido:

1. Recibir desde la aplicación móvil un Firebase Auth ID Token y un Firebase App Check Token.
2. Validar el formato, la unicidad y el tamaño de ambas cabeceras.
3. Verificar App Check y rechazar aplicaciones no válidas.
4. Verificar Firebase Authentication, incluida la revocación, y obtener el identificador del usuario en el servidor.
5. Construir un principal autenticado inmutable.
6. Comprobar la autorización para la capacidad solicitada y los datos afectados.
7. Aplicar límites, validaciones y reglas de negocio.
8. Ejecutar la lectura o preparar la propuesta de escritura.
9. Devolver únicamente los datos necesarios para responder.

Firebase App Check es obligatorio en la frontera implementada y no reemplaza la autenticación ni la autorización por recurso. La conexión con el proyecto real y su activación en las aplicaciones móviles permanecen pendientes. El contrato completo se documenta en [Autenticación y verificación de la aplicación](AUTHENTICATION.md).

La frontera transversal de transporte también está implementada: reserva `/api/v1` para capacidades funcionales, genera correlación por petición, normaliza errores públicos, aplica límites de cuerpo y timeout, y emite logs JSON con campos permitidos. El contrato completo se documenta en [Frontera HTTP, errores y observabilidad](HTTP-BOUNDARY.md).

## 4. Límites del modelo

El comportamiento se limitará mediante varias capas complementarias:

- Catálogo cerrado de capacidades.
- Esquemas estrictos para argumentos y resultados.
- Validación determinista en la API.
- Políticas de autorización independientes del modelo.
- Límites de frecuencia, volumen y coste.
- Registro de decisiones y operaciones sin almacenar contenido sensible innecesario.
- Respuestas controladas para solicitudes fuera de alcance.

El modelo puede proponer qué capacidad utilizar, pero la API decide si esa capacidad existe, si los argumentos son válidos y si el usuario puede ejecutarla.

## 5. Respuestas basadas en datos verificables

Las respuestas sobre actividad, perfil o salud deben basarse en datos recuperados por la API y no en información inventada por el modelo.

Ejemplo de resultado estructurado candidato:

```json
{
  "periodo": "ultimos_7_dias",
  "paseos": 8,
  "distancia_metros": 18420,
  "duracion_segundos": 12600
}
```

A partir de ese resultado, el modelo puede redactar una explicación comprensible. Los cálculos, agregaciones, conversiones y comparaciones relevantes deben realizarse de forma determinista en la API para que sean reproducibles y comprobables.

Cuando falten datos o su calidad sea insuficiente, la respuesta deberá indicarlo claramente en lugar de completar los huecos mediante suposiciones.

## 6. Solicitudes fuera de alcance

La API y el modelo deben reconocer límites funcionales y de seguridad.

| Tipo de solicitud | Comportamiento esperado |
| --- | --- |
| Datos de otra persona o de otro perro sin autorización | Rechazar sin revelar si esos datos existen |
| Diagnóstico o tratamiento veterinario | Explicar el límite y recomendar atención veterinaria cuando proceda |
| Operación destructiva o de alto impacto | No ejecutarla directamente; aplicar el flujo específico de confirmación o rechazarla |
| Instrucciones para ignorar políticas o revelar configuración interna | Ignorarlas y mantener las restricciones del sistema |
| Petición no cubierta por el catálogo | Explicar qué capacidades sí están disponibles |

El tono de rechazo debe ser claro, breve y útil, sin exponer detalles internos que faciliten eludir las protecciones.

## 7. Escrituras con confirmación explícita

Las operaciones que cambien datos no deben ejecutarse por una interpretación implícita del diálogo.

Flujo objetivo:

```text
Usuario solicita un cambio
  → modelo interpreta la intención
  → API valida y crea una propuesta pendiente
  → aplicación muestra una tarjeta editable
  → usuario revisa y confirma una versión exacta
  → API vuelve a validar autorización y contenido
  → operación idempotente
  → confirmación del resultado
```

La propuesta pendiente deberá incluir una caducidad, una versión y una clave de idempotencia. Si el usuario edita la propuesta, la confirmación se aplicará a la versión visible y no a una versión anterior conservada en el diálogo.

Las operaciones especialmente sensibles pueden quedar excluidas del chatbot aunque exista confirmación.

## 8. Papel del historial de conversación

El historial permite mantener continuidad lingüística y referencias recientes, pero no es una fuente canónica de identidad, permisos ni datos del producto.

La API deberá enviar al modelo solo el contexto necesario y limitar su tamaño. Los hechos persistentes deben recuperarse de sus fuentes autorizadas en cada operación relevante.

El historial no debe utilizarse como:

- Sustituto de Firebase Authentication.
- Almacén clínico o de salud.
- Registro definitivo de cambios.
- Fuente única para cálculos o estadísticas.

## 9. Componentes internos propuestos

```text
Cliente iOS / Android
  ├─ autenticación
  ├─ interfaz conversacional
  ├─ visualización de resultados estructurados
  └─ confirmación explícita de cambios

API de Dappy Dogs
  ├─ autenticación y autorización
  ├─ orquestador conversacional
  ├─ catálogo de capacidades
  ├─ validación de contratos
  ├─ servicios de dominio
  ├─ acceso controlado a Firebase
  ├─ operaciones pendientes e idempotencia
  ├─ límites de uso
  └─ observabilidad y auditoría

Proveedor del modelo
  ├─ interpretación de intención
  ├─ selección de capacidades permitidas
  └─ redacción de respuestas
```

Los servicios de dominio deben aislar la lógica de actividad, perfil, relaciones sociales, mensajería y futuras funciones de salud. De este modo, el chatbot consume contratos del producto y no la estructura física de Firestore.

## 10. Reparto de responsabilidades

| Responsabilidad | Modelo | API de Dappy Dogs |
| --- | :---: | :---: |
| Interpretar lenguaje natural | Sí | Apoya mediante contexto y contratos |
| Redactar respuestas | Sí | Filtra y valida el resultado final cuando sea necesario |
| Autenticar al usuario | No | Sí |
| Autorizar el acceso | No | Sí |
| Consultar Firebase | No | Sí |
| Calcular estadísticas verificables | No | Sí |
| Aplicar reglas de negocio | No | Sí |
| Persistir cambios | No | Sí, tras validación y confirmación |
| Limitar coste y frecuencia | No | Sí |
| Registrar operaciones | No | Sí |

## 11. Flujo técnico de una consulta

1. La aplicación envía el mensaje con sus credenciales de Firebase Authentication y App Check.
2. La API valida ambas credenciales y obtiene la identidad efectiva.
3. El orquestador prepara instrucciones, contexto mínimo y catálogo de capacidades.
4. El modelo responde directamente o solicita una capacidad.
5. La API valida el nombre de la capacidad y sus argumentos.
6. La capa de autorización comprueba el acceso al recurso solicitado.
7. El servicio de dominio consulta Firebase y realiza cálculos deterministas.
8. La API devuelve al modelo un resultado estructurado y reducido.
9. El modelo redacta una respuesta basada en ese resultado.
10. La API aplica controles finales de formato, seguridad y observabilidad.
11. La aplicación presenta texto y, cuando corresponda, componentes estructurados.

Si la intención implica una escritura, el flujo termina primero en una propuesta pendiente. La persistencia se realiza únicamente tras una confirmación explícita posterior.

## 12. Diseño inicial del catálogo

Antes de conectar un modelo con datos reales debe definirse un catálogo reducido de preguntas y acciones prioritarias. Para cada elemento se documentará:

- Intención de producto.
- Datos mínimos necesarios.
- Capacidad interna que los proporciona.
- Esquema de entrada y salida.
- Reglas de autorización.
- Respuesta cuando falten datos.
- Condiciones de rechazo.
- Necesidad o no de confirmación.
- Casos de prueba funcionales, de seguridad y de privacidad.

El primer catálogo debe ser deliberadamente pequeño. Se ampliará cuando cada capacidad anterior tenga contratos estables, pruebas y observabilidad suficiente.

## 13. Criterios transversales

### Privacidad

Se minimizarán los datos enviados al proveedor del modelo y se evitará incluir identificadores o atributos que no sean necesarios para responder. La retención y el tratamiento deberán documentarse antes de operar con datos reales.

### Seguridad

Toda salida del modelo se tratará como entrada no confiable. Las validaciones, permisos y reglas se ejecutarán en código controlado por el producto.

### Observabilidad

Se medirán latencia, errores, capacidades solicitadas, rechazos, consumo y calidad de respuesta. Los registros deberán excluir o enmascarar contenido sensible.

### Evolución de contratos

La API conversacional no debe depender de nombres de colecciones o campos de Firestore en sus contratos públicos. Una capa de dominio permitirá corregir o migrar la base de datos sin acoplar las aplicaciones móviles ni el modelo a su estructura interna.

## 14. Siguientes decisiones de arquitectura

Antes de implementar el núcleo conversacional deben cerrarse, al menos:

1. Casos de uso que formarán el primer catálogo.
2. Integración operativa del contrato de autenticación implementado con ambas aplicaciones y el entorno Firebase autorizado.
3. Modelo de autorización por recurso y relación.
4. Contratos de dominio derivados de los datos existentes.
5. Proveedor y modelo de lenguaje.
6. Estrategia de transmisión de respuestas.
7. Política de conservación de conversaciones y telemetría.
8. Flujo de confirmación para cada tipo de escritura permitido.
9. Evaluaciones y umbrales mínimos de calidad y seguridad.

La autenticación se documenta en [Autenticación y verificación de la aplicación](AUTHENTICATION.md). La estructura actual de Firestore y sus limitaciones conocidas se documentan por separado en [Base de datos de Firestore](FIRESTORE-DATABASE.md).
