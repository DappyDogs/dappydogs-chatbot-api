# Base de datos de Firestore

## Estado del documento

Esta es una primera fotografía de la base de datos utilizada actualmente por Dappy Dogs. Los recuentos se verificaron el 19 de noviembre de 2026 mediante consultas de solo lectura sobre las colecciones raíz.

El contenido y los esquemas todavía no se han analizado de forma exhaustiva. Las descripciones funcionales basadas únicamente en el nombre de una colección se marcan como interpretaciones preliminares y deberán confirmarse con la copia local.

## Alcance del recuento

- Se han identificado nueve colecciones raíz.
- El total verificado es de 5.717 documentos raíz.
- El recuento no incluye documentos alojados exclusivamente en subcolecciones.
- No se han modificado datos para obtener esta información.
- No se incluyen identificadores de documentos, valores personales ni ejemplos procedentes de usuarios reales.

## Inventario inicial

| Colección | Documentos raíz | Contenido o función preliminar | Nivel de certeza |
| --- | ---: | --- | --- |
| `Friends` | 171 | Relaciones de amistad entre usuarios o perfiles. Quedan por confirmar el modelo de estados, la dirección de la relación y la propiedad de cada registro. | Inferido por el nombre |
| `LikesReceived` | 870 | Índice o registro de interacciones de tipo «me gusta» recibidas. Quedan por confirmar el recurso afectado y su relación con usuarios y perros. | Inferido por el nombre |
| `LikesSended` | 498 | Índice o registro de interacciones de tipo «me gusta» enviadas. `LikesSended` es el nombre real de la colección y conserva una denominación no normalizada. | Inferido por el nombre |
| `Messages` | 0 | Espacio destinado a mensajes. El recuento raíz es cero; debe comprobarse si los mensajes están en subcolecciones o si esta estructura ya no se utiliza. | Nombre conocido; estructura pendiente |
| `MessagesIndices` | 7 | Índices o referencias para localizar conversaciones o mensajes. Deben confirmarse sus claves, relaciones y vigencia. | Inferido por el nombre |
| `Notifications` | 141 | Notificaciones dirigidas a usuarios. Quedan por identificar tipos, estados, caducidad y relación con otros recursos. | Inferido por el nombre |
| `RoutePoops` | 45 | Eventos o marcadores asociados previsiblemente a deposiciones registradas durante rutas. Debe confirmarse su vínculo exacto con rutas, usuarios y perros. | Inferido por el nombre |
| `Routes` | 3.087 | Paseos o rutas registradas, previsiblemente con información temporal, distancia, recorrido y referencias al usuario o al perro. El esquema exacto está pendiente de inventario. | Función general conocida; esquema pendiente |
| `Users` | 898 | Perfiles y estado de usuarios, propietarios y perros. La adaptación de perfil identifica siete firmas estructurales relevantes y proyecta únicamente nombre, nacimiento y catálogos del perro. | Estructura relevante analizada |
| **Total** | **5.717** | Documentos contabilizados en las colecciones raíz. | Verificado |

## Observaciones iniciales

### Nombres y límites de dominio

La base actual mezcla nombres de entidades principales, índices auxiliares y eventos derivados en el mismo nivel raíz. Antes de diseñar la API del chatbot será necesario separar conceptualmente:

- Entidades canónicas del producto.
- Relaciones entre usuarios o perfiles.
- Datos de actividad y rutas.
- Mensajería y notificaciones.
- Índices o proyecciones auxiliares.
- Eventos específicos asociados a una ruta.

Los nombres físicos de Firestore no deben convertirse directamente en contratos públicos de la API. La API deberá exponer modelos de dominio estables y encargarse de traducirlos a la estructura persistida.

### Colecciones vacías y subcolecciones

El valor cero de `Messages` solo demuestra que no hay documentos directamente en su raíz. No permite concluir que no existan mensajes: Firestore puede mantener subcolecciones bajo referencias conocidas por la aplicación. Esta posibilidad debe verificarse durante el inventario jerárquico.

### Datos de salud

En este recuento no se ha identificado una colección raíz dedicada explícitamente a historiales de salud. Cualquier modelo futuro de salud deberá tratarse como diseño nuevo hasta que el análisis demuestre que existen datos equivalentes en otra ubicación.

### Sensibilidad de los datos

Es previsible que `Users`, `Routes`, relaciones sociales, mensajes y notificaciones contengan información personal o permitan inferir hábitos y ubicaciones. El análisis deberá minimizar la exposición de valores reales y centrarse en esquemas, tipos, frecuencias y calidad de datos.

## Análisis pendiente sobre la copia local

La siguiente revisión ampliará este documento con resultados agregados y sin datos personales. Para cada colección se estudiará:

1. Campos presentes y porcentaje de aparición.
2. Tipos reales y variaciones de tipo por campo.
3. Valores nulos, vacíos, ausentes o malformados.
4. Formato y unidad de fechas, duraciones, distancias y coordenadas.
5. Referencias entre documentos y reglas de propiedad.
6. Subcolecciones y profundidad de la jerarquía.
7. Catálogos de valores y estados de ciclo de vida.
8. Duplicados, datos obsoletos y posibles inconsistencias.
9. Campos sensibles que deban omitirse del contexto del modelo.
10. Necesidades de índices y consultas para los casos de uso del chatbot.

## Entregables previstos tras el análisis

- Diccionario de datos por colección.
- Mapa de relaciones entre entidades.
- Inventario de subcolecciones.
- Informe de calidad y riesgos de migración.
- Contratos de dominio que oculten la estructura física de Firestore.
- Recomendaciones para lecturas eficientes y autorizadas desde la API.
- Propuesta separada para cualquier dato nuevo que requiera el chatbot.

Hasta completar ese análisis, las cifras de la tabla son verificadas, pero las descripciones de campos, relaciones y ciclos de vida deben considerarse provisionales.

## Adaptación implementada para `Users`

La API dispone de un modelo canónico mínimo y adaptadores de solo lectura para perfil. La revisión agregada confirma siete firmas estructurales relevantes entre los 898 documentos. Los campos ausentes, nulos, vacíos, inválidos y los catálogos desconocidos se conservan como diagnósticos tipados sin corregir Firestore.

La fecha `dogDate` presenta 818 cadenas de diez caracteres, una de nueve, una cadena literal no numérica de cuatro caracteres y 42 valores nulos; existen además documentos sin el campo. La adaptación valida cada representación y no asume que una longitud implica por sí sola un valor correcto.

El contrato detallado, los campos excluidos y las dependencias todavía abiertas se encuentran en [Acceso al perfil de usuario](USER-PROFILE.md).
