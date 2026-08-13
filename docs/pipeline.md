# Documentación del pipeline de evaluación de textos alternativos

## Objetivo

`eval-texto-alternativo` implementa un pipeline o flujo ordenado y secuencial de módulos para realizar comparaciones entre producciones de texto alternativo generadas mediante IA y sus correspondientes correcciones humanas.

El pipeline está organizado en cinco etapas:

```text
01 pair
   ↓
02 preprocess
   ↓
03 build_document
   ↓
04 eval
   ↓
05 export
```

## Step 01 — `pair`

Archivo: `pipeline/step_01_pair.py`

### Responsabilidad

Relacionar cada producción de IA con su correspondiente corrección humana.

La organización actual es:

```text
data/
├── ia/
│   ├── original-01.md
│   └── ...
└── human/
    ├── corregido-01.md
    └── ...
```

### Interfaz `load_pairs(start, end)`

Carga los pares correspondientes al intervalo solicitado y entrega al pipeline los textos IA/humano asociados a un identificador.

La separación de esta etapa evita que las etapas posteriores tengan que conocer los nombres de los archivos ni las reglas utilizadas para asociarlos.

## Step 02 — `preprocess`

Archivo: `pipeline/step_02_preprocess.py`

### Responsabilidad

Eliminar elementos de sintaxis Markdown o de formato que no representan contenido relevante para este dominio, como el frontmatter, las etiquetas HTML y los backticks que no forman parte del contenido del material visual.

Esto permite que el siguiente módulo, `build_document`, no tenga que modelar construcciones de formato que no forman parte del tipo de contenido que se quiere evaluar.

### Interfaz `preprocess(text)`

Prepara el texto antes de construir el modelo `Document`.

El preprocesamiento separa la preparación del texto de la interpretación estructural.

El mismo procesamiento se aplica a IA y humano:

```python
# en run_pipeline.py:

ia = preprocess(ia_raw)
human = preprocess(human_raw)
```

## Step 03 — `build_document`

Archivo: `pipeline/step_03_build_document.py`

### Responsabilidad

Transformar cada documento preprocesado en un objeto `Document` que represente su estructura y contenido.

### Interfaz `build_document(text)`

Transforma el texto preprocesado en un objeto `Document`.

El objeto posee dos representaciones principales:

```text
Document
├── structure
└── content
```

### Estructura

Es una colección ordenada de elementos:

```python
(tipo, valor)
```

Los tipos actuales incluyen:

```text
h1
h2
h3
landmark
label
paragraph
list
```

La colección ordenada permite conservar el orden y evaluar la organización del documento.

Las listas son una unidad estructural. Sus elementos internos se conservan dentro de la lista:

```python
(
    "list",
    [
        "Texto:",
        "Contenido del primer elemento",
        "Contenido del segundo elemento",
    ],
)
```

### Contenido

Agrupa el contenido por tipo:

```python
{
    "headings": {
        "h1": [...],
        "h2": [...],
        "h3": [...],
    },
    "labels": [...],
    "landmarks": [...],
    "paragraphs": {...},
    "lists": [...],
}
```

Esta representación permite que los evaluadores trabajen con colecciones específicas sin volver a interpretar el texto original.

### Definición de párrafo para la comparación

En este pipeline, un párrafo es una **unidad de texto utilizada como unidad de comparación**.

Esta definición es operativa: no busca establecer qué constituye un párrafo desde el punto de vista lingüístico, tipográfico o editorial, sino determinar qué fragmento de texto se considera una unidad al comparar las producciones de IA con las correcciones humanas.

Un salto de línea no implica necesariamente el comienzo de un nuevo párrafo. Puede formar parte de la organización deliberada del texto, como ocurre, por ejemplo, en determinados textos narrativos, poéticos o en otras formas de escritura donde la distribución de las líneas tiene un significado propio.

También puede ocurrir que una producción de IA introduzca saltos de línea dentro de una unidad que conceptualmente corresponde a un mismo fragmento de texto.

Por ejemplo:

```text
Las mujeres
también fueron
protagonistas
en la historia
de la tecnología.
```

El pipeline puede tratar estas líneas como una única unidad textual para la comparación cuando la estructura interpretada por `build_document` así lo determina.

### `normalize_text(text)`

Normaliza el texto utilizado para las comparaciones y para la generación de claves de párrafos.

La normalización permite que diferencias que no se consideran relevantes para esta etapa, como mayúsculas, acentos, espacios o signos de puntuación, no afecten determinadas comparaciones textuales.

### `make_paragraph_key(text)`

Genera una clave para identificar cada párrafo a partir de una representación normalizada del texto.

La clave combina una parte legible derivada de las primeras palabras con un hash corto del texto completo normalizado.

### Uso de un hash corto

Los párrafos necesitan una clave que permita identificarlos durante las comparaciones y conservar una referencia legible para inspeccionar los resultados.

Utilizar solamente las primeras palabras no garantiza que dos párrafos tengan identificadores diferentes:

```text
Las mujeres también fueron protagonistas...
Las mujeres también fueron protagonistas durante...
```

Podrían compartir la misma clave inicial.

Utilizar todo el párrafo como clave produciría identificadores poco manejables.

La solución utilizada combina una parte legible con un hash corto:

```text
texto completo
      ↓
normalización
      ↓
primeras palabras ───────┐
                         ├── clave
hash del texto completo ─┘
```

Por ejemplo:

```text
las-mujeres-tambien-fueron-protagonistas-779411c8
```

La primera parte facilita la inspección humana. El hash corto permite diferenciar textos completos que comparten el mismo comienzo.

El hash **no es una medida de similitud**. Es solamente un identificador técnico.

La clave se genera sobre el texto normalizado. Por eso, diferencias que la normalización elimina no producen claves diferentes.

Si dos párrafos tienen exactamente el mismo contenido normalizado, también generan la misma clave. El método no pretende resolver mediante el hash la existencia de múltiples ocurrencias de un mismo texto.

## Step 04 — `eval`

Archivo: `pipeline/step_04_eval.py`

### Responsabilidad

Comparar la producción de IA con la corrección humana y producir resultados de evaluación sobre su estructura y contenido.

La corrección humana se utiliza como referencia porque la persona que realizó la revisión y corrección contrastó la producción automática con los carteles originales.

### Interfaz `evaluate_documents(ia, human)`

Coordina:

```text
evaluate_structure()
evaluate_content()
```

### Evaluación estructural

#### `evaluate_structure(ia, human)`

Compara `Document.structure` de IA y humano.

Actualmente considera:

- cantidad total de elementos
- cantidad de H1, H2 y H3
- cantidad de landmarks
- cantidad de labels
- cantidad de párrafos
- cantidad de listas
- coincidencias de tipo según posición

#### `count_structure(structure)`

Cuenta cuántos elementos de cada tipo aparecen en una estructura.

Por ejemplo:

```python
[
    ("h1", "Título"),
    ("paragraph", "Texto"),
    ("paragraph", "Otro texto"),
]
```

produce:

```python
{
    "h1": 1,
    "paragraph": 2,
}
```

#### `describe_difference(label, ia_count, human_count)`

Transforma una diferencia numérica en un mensaje descriptivo que expresa la cantidad generada por IA en comparación con la corrección humana.

#### `compare_order(ia_structure, human_structure)`

Compara el tipo de elemento que aparece en cada posición.

Por ejemplo:

```text
IA:     h1 → h2 → paragraph
Humano: h1 → landmark → paragraph
```

Produce dos posiciones coincidentes de tres comparables.

Actualmente, es una comparación posicional simple. No realiza alineación estructural avanzada cuando existen inserciones, omisiones o desplazamientos.

### Evaluación de contenido

#### `evaluate_content(ia, human)`

Su objetivo actual es determinar qué unidades textuales de la IA pueden asociarse con unidades de la corrección humana.

La evaluación mide **correspondencia textual**. No determina por sí misma si dos frases expresan semánticamente la misma idea.

### Comparación de párrafos

#### El problema

La comparación de párrafos presentó varias dificultades:

- un mismo texto puede aparecer con diferencias de mayúsculas o puntuación
- un párrafo puede haber sido corregido
- un párrafo puede haber sido dividido
- varios párrafos pueden haber sido reorganizados
- la IA puede producir un párrafo que no tenga correspondencia
- la corrección humana puede incorporar contenido que la IA no transcribió
- dos párrafos pueden comenzar con las mismas palabras sin ser iguales
- los documentos no necesariamente conservan la misma posición para una unidad textual equivalente

Por estas particularidades, una comparación basada únicamente en la posición no resulta suficiente.

La solución actual utiliza dos colecciones de párrafos pendientes:

```text
párrafos IA ───────┐
                   ├── búsqueda de correspondencias
párrafos humanos ──┘
                   ↓
              pendientes
```

La corrección humana se toma como referencia durante esta asociación.

Cada párrafo es evaluado antes de ser retirado de las colecciones pendientes. Cuando se establece una correspondencia, ambos párrafos se eliminan de sus respectivas colecciones. De esta manera, un mismo párrafo humano no puede reutilizarse para asociarlo con varios párrafos IA.

#### Coincidencia exacta normalizada

La primera búsqueda utiliza las claves generadas para los párrafos.

Si una clave aparece tanto en IA como en humano:

1. se considera una **coincidencia exacta normalizada**
2. se registra una similitud de `1.0`
3. se retiran ambos párrafos de las colecciones pendientes

No equivale a decir que los textos originales son idénticos, carácter por carácter.

Por ejemplo, diferencias de mayúsculas, acentos, espacios o signos de puntuación pueden desaparecer durante la normalización.

La coincidencia exacta normalizada puede entenderse como el caso particular en que la representación normalizada coincide completamente. No se utiliza un umbral de `0.99` para representar este caso: la coincidencia se determina mediante igualdad de la clave generada a partir del texto normalizado.

#### Fuzzy matching

Una vez agotadas las coincidencias por clave, quedan párrafos pendientes.

La implementación actual recorre los párrafos humanos pendientes y utiliza cada uno como referencia para buscar una posible correspondencia entre los párrafos IA pendientes.

Conceptualmente:

```text
párrafo humano de referencia
        ↓
comparar con cada párrafo IA pendiente
        ↓
calcular similitud textual
        ↓
terminar recorrido
        ↓
¿mejor coincidencia alcanza el umbral?
   ├── sí → registrar correspondencia
   └── no → conservar como no coincidente
```

La comparación no se detiene simplemente al alcanzar el umbral durante el recorrido.

Para seleccionar la mejor correspondencia disponible, se completa la comparación con los candidatos IA pendientes y se conserva el candidato que obtuvo la mayor similitud.

Si la mejor similitud alcanza o supera el umbral:

1. se identifica el mejor candidato
2. se registra la coincidencia aproximada
3. se conserva la similitud obtenida
4. se retiran ambos párrafos de las colecciones pendientes

Si ningún candidato alcanza el umbral, el párrafo humano permanece sin correspondencia.

Este procedimiento se repite mientras existan elementos pendientes.

Por lo tanto, el umbral funciona como un criterio para aceptar o rechazar la mejor correspondencia encontrada, pero no como un mecanismo de corte anticipado del recorrido.

Una posible mejora futura sería incorporar mecanismos de preselección de candidatos para reducir comparaciones innecesarias cuando los conjuntos sean mayores.

### Comparación textual con `SequenceMatcher`

La comparación fuzzy utiliza `difflib.SequenceMatcher`, una clase de la biblioteca estándar de Python diseñada para comparar secuencias y obtener un valor de similitud.

En este pipeline se utiliza para comparar secuencias de caracteres correspondientes a párrafos previamente normalizados.

Su funcionamiento puede resumirse en tres pasos:

1. **Cálculo de similitud:** toma un párrafo humano como referencia y calcula su similitud con cada párrafo IA pendiente mediante `SequenceMatcher(None, texto_humano, texto_ia).ratio()`. Ambos textos se comparan después de aplicar la normalización correspondiente.

2. **Identificación de la mejor opción:** al recorrer los párrafos IA pendientes, conserva el candidato que obtiene el valor de similitud más alto (`best_similarity`).

3. **Aplicación del umbral:** una vez finalizado el recorrido, si la mejor similitud alcanza o supera `FUZZY_THRESHOLD`, se registra la correspondencia entre ambos párrafos. De lo contrario, el párrafo humano permanece sin correspondencia.

La comparación actual es:

```text
texto normalizado
       ↓
secuencia de caracteres
       ↓
SequenceMatcher
       ↓
valor de similitud
```

No se realiza una comparación palabra por palabra ni token por token en el sentido de un análisis lingüístico.

Tampoco se realiza comparación semántica. El método no intenta reconocer automáticamente que dos textos expresan la misma idea utilizando palabras diferentes.

Una evaluación semántica requeriría otro tipo de método y corresponde a una posible línea de investigación posterior.

La búsqueda exhaustiva compara cada párrafo humano pendiente con los párrafos IA pendientes. Si existen `N` párrafos humanos y `M` párrafos IA, la etapa de búsqueda realiza hasta `N × M` comparaciones de pares.

Para conjuntos de tamaño similar, esto se aproxima a `O(N²)` en cantidad de pares comparados. El costo efectivo también depende de la longitud de los textos procesados por `SequenceMatcher`.

La estrategia resulta razonable para el tamaño del conjunto utilizado en esta etapa, pero podría requerir una optimización si el volumen de documentos aumenta considerablemente.

### Definición de similitud

La similitud producida por `SequenceMatcher` es una medida de semejanza entre secuencias de caracteres.

No representa un porcentaje de palabras correctas ni un porcentaje de fidelidad respecto de la imagen.

Por ejemplo:

```text
similitud = 0.85
```

no significa:

```text
85 % de fidelidad
```

Significa que la función utilizada encontró un determinado grado de similitud entre las dos secuencias de caracteres comparadas.

La interpretación de ese valor en términos de calidad del texto es una cuestión que todavía debe investigarse.

### Umbral fuzzy

El valor utilizado es:

```python
FUZZY_THRESHOLD = 0.70
```

Este valor es un **umbral heurístico inicial**. Fue elegido para poner en funcionamiento la primera versión del método y todavía no ha sido validado empíricamente.

El umbral representa la similitud mínima utilizada para aceptar una correspondencia aproximada.

En términos generales:

```text
umbral más bajo
    → más asociaciones posibles
    → mayor posibilidad de asociaciones incorrectas

umbral más alto
    → menos asociaciones
    → mayor cantidad de elementos sin correspondencia
```

Determinar cuál es un valor adecuado y qué representa ese valor en términos de calidad de la correspondencia es una cuestión pendiente.

Una posible investigación posterior consiste en variar sistemáticamente el umbral y analizar cómo cambian las correspondencias, los emparejamientos incorrectos y los elementos sin correspondencia.

### Elementos sin correspondencia

Los elementos que quedan pendientes al finalizar las comparaciones se clasifican como:

```text
unmatched_ia
unmatched_human
```

Esto permite identificar dos situaciones diferentes:

- contenido producido por IA que no encuentra una unidad correspondiente en la corrección humana
- contenido presente en la corrección humana que no encuentra una unidad correspondiente en la producción de IA

Estas categorías tampoco permiten determinar por sí mismas la exactitud de la transcripción ni la fidelidad de la descripción. Requieren investigación posterior.

### Resultado

La función de comparación de párrafos devuelve:

```python
{
    "exact_matches": [...],
    "fuzzy_matches": [...],
    "unmatched_ia": [...],
    "unmatched_human": [...],
}
```

Las claves de párrafo son identificadores internos y no constituyen resultados de la evaluación.

## Step 05 — `export`

Archivo: `pipeline/step_05_export.py`

### Responsabilidad

Transformar los resultados de evaluación en formatos de almacenamiento y análisis.

### `flatten_results(results)`

Convierte los resultados anidados en filas planas para CSV.

El aplanamiento pertenece a la exportación porque es una necesidad del formato CSV, no de la evaluación.

### Interfaz `export_csv(rows, path)`

Escribe las filas planas en CSV mediante el módulo estándar `csv`.

No calcula métricas; solamente serializa los datos recibidos.

### Interfaz `export_json(rows, path)`

Guarda los resultados estructurados en JSON.

### `generate_summary(results)`

Genera estadísticas agregadas del conjunto.

### Interfaz `export_summary(summary, path)`

Guarda el resumen estadístico como JSON.

## Orquestación — `run_pipeline.py`

Archivo: `pipeline/run_pipeline.py`

### Responsabilidad

Orquestar la ejecución de las cinco etapas del pipeline.

### Flujo

```text
load_pairs()
    ↓
preprocess()
    ↓
build_document()
    ↓
evaluate_documents()
    ↓
exportación
```

Para cada par:

```python
ia = preprocess(ia_raw)
human = preprocess(human_raw)

ia_document = build_document(ia)
human_document = build_document(human)

comparison = evaluate_documents(
    ia_document,
    human_document,
)
```

Después se conserva el identificador del documento y se acumulan los resultados.

Finalmente se generan:

```text
comparison.csv
comparison.json
summary.json
```

## Próximos pasos

Entre las líneas de trabajo previstas se encuentran:

1. ejecutar y revisar la evaluación sobre los 53 pares
2. analizar coincidencias y no coincidencias
3. estudiar el comportamiento del umbral fuzzy
4. validar las métricas actuales
5. desarrollar criterios específicos para evaluar la exactitud de la transcripción
6. desarrollar criterios específicos para evaluar la fidelidad de las descripciones de imágenes
7. contrastar la metodología con bibliografía y proyectos existentes
8. estudiar posibles mejoras en la búsqueda de correspondencias
9. integrar los resultados en la plataforma general