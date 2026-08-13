# Evaluación de textos alternativos

![Python](https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/tests-pytest-blue?logo=pytest&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-green?logo=node.js&logoColor=white)
![Eleventy](https://img.shields.io/badge/Eleventy-orange?logo=eleventy&logoColor=white)

Proyecto para comparar producciones de texto alternativo generadas mediante inteligencia artificial con versiones revisadas y corregidas por una persona.

El proyecto surge como parte de la experiencia de desarrollo de una plataforma de textos alternativos para materiales visuales educativos.

Como etapa inicial se trabajó con una actividad del TIVU 2026. Se generaron transcripciones y descripciones automáticas que posteriormente fueron revisadas y corregidas por una persona usando los carteles originales como fuente de verdad. El conjunto actual contiene **53 pares de documentos**.

## Objetivo

El proyecto busca obtener mediciones sobre dos aspectos del texto alternativo generado por IA:

- **Estructura:** correspondencia con la estructura que se definió y estandarizó para la plataforma
- **Contenido:** correspondencia entre las unidades textuales producidas por la IA y las de la corrección humana, como una primera aproximación antes de estudiar la fidelidad y certeza respecto del material visual

La evaluación se encuentra en una etapa inicial y se desarrolla de manera iterativa a partir de la experiencia, la identificación de problemas y la mejora de los criterios utilizados.

## Origen de la estructura

La estructura utilizada por la plataforma no fue proporcionada inicialmente a la IA.

Durante una primera experiencia se revisaron las producciones generadas automáticamente y se identificaron elementos que resultaban útiles junto con otros que requerían corrección o unificación. A partir de esa experiencia se definió y documentó una estructura estandarizada para los textos publicados en la plataforma.

Posteriormente, este criterio se replicó durante la revisión de los documentos restantes.

La estructura utilizada actualmente incluye:

- **H1** para el título del contenido
- **H2** para secciones de orientación
- **H3** para subdivisiones cuando corresponda
- **Landmarks**, representados mediante corchetes, para indicar contexto, ubicación o agrupación dentro del material
- **Labels** para elementos organizativos dentro de una sección
- **Párrafos** para unidades textuales
- **Listas** cuando forman parte de la organización del material

Se utilizan los términos **landmark** y **label** porque permite mantener una correspondencia con la terminología técnica utilizada en accesibilidad web y tecnologías de asistencia. 

La estructura está documentada en la Plataforma de textos alternativos.

## Datos de evaluación

El conjunto actual contiene 53 pares:

```text
data/
├── ia/
│   ├── original-01.md
│   ├── original-02.md
│   └── ...
└── human/
    ├── corregido-01.md
    ├── corregido-02.md
    └── ...
```

Los archivos `ia/` contienen las producciones originales generadas automáticamente.

Los archivos `human/` contienen las versiones revisadas, corregidas y estandarizadas por una persona.

La corrección humana se realiza contrastando la producción automática con la imagen original del material. Por este motivo, las versiones humanas constituyen actualmente la referencia utilizada por los evaluadores automáticos.

## Pipeline

El procesamiento se organiza en cinco etapas:

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

Conceptualmente:

```text
datos
  ↓
asociación de pares
  ↓
preprocesamiento
  ↓
construcción de Document
  ↓
evaluación
  ├── estructura
  └── contenido
       └── comparación de párrafos
  ↓
exportación
  ├── CSV
  ├── JSON
  └── resumen JSON
```

La descripción detallada de cada etapa se encuentra en `docs/pipeline.md`.

## Evaluadores

En este proyecto, **evaluador** refiere a una función de evaluación. No se utiliza el término para referirse a las personas que revisan las producciones de IA.

Actualmente, se implementan dos funciones evaluadoras dentro de `step_04_eval.py`:

1. **Evaluador de estructura**
2. **Evaluador de contenido**

La corrección humana es la referencia utilizada por ambas funciones evaluadoras.

### Evaluación de estructura

El evaluador de estructura considera:

- H1
- H2
- H3
- landmarks
- labels
- párrafos
- listas

Se analizan cantidades y el orden de los tipos de elementos.

La comparación de orden es actualmente posicional y no intenta resolver alineaciones estructurales más complejas cuando existen inserciones, omisiones o desplazamientos.

### Evaluación de contenido

Su objetivo actual es determinar qué unidades textuales de la producción de IA pueden asociarse con unidades de la corrección humana.

Los párrafos reciben un tratamiento específico porque la correspondencia entre ambos documentos puede verse afectada por distintas situaciones:

- un párrafo puede presentar diferencias de redacción respecto de su correspondiente
- un párrafo puede haber sido dividido o combinado durante la corrección
- un párrafo puede haber sido reorganizado respecto de su posición original
- un párrafo puede compartir solamente una parte de su contenido con otro
- un párrafo puede no tener una correspondencia identificable en el otro documento

## Tecnologías

El pipeline está implementado en Python 3 y utiliza principalmente la biblioteca estándar:

- `pathlib` para manejo de archivos
- `dataclasses` para el modelo `Document`
- `re` y `unicodedata` para procesamiento y normalización textual
- `hashlib` para identificadores de párrafos
- `difflib.SequenceMatcher` para similitud textual
- `csv` y `json` para exportación
- `pytest` para testing

Para la interfaz gráfica y visualización de resultados:

- `Eleventy`

Por el momento, se encuentra en desarrollo.

## Ejecución

El pipeline completo se ejecuta mediante:

```shell
python pipeline/run_pipeline.py
```

Los resultados se generan en `outputs/`.

## Tests

El proyecto utiliza `pytest` y organiza los tests según las etapas del pipeline:

```text
tests/
├── test_01_pair.py
├── test_02_preprocess.py
├── test_03_build_document.py
├── test_04_eval.py
└── test_05_export.py
```

La estrategia de pruebas y los ejemplos de transformación de texto a `Document` se encuentran en `docs/tests.md`

Para ejecutar la suite:

```shell
./scripts/test.sh
```

## Resultados

```text
outputs/
├── comparison.json
├── comparison.csv
└── summary.json
```

### `comparison.json`

Conserva los resultados completos y estructurados.

### `comparison.csv`

Contiene métricas aplanadas para análisis tabular. No contiene los textos completos de las coincidencias de párrafos.

### `summary.json`

Contiene estadísticas agregadas del conjunto.

## Estado del proyecto

El proyecto se encuentra en una etapa de desarrollo iterativo.

El trabajo actual se concentra en:

1. consolidar la evaluación estructural
2. validar la comparación de contenido
3. analizar los resultados sobre los 53 documentos
4. estudiar el comportamiento de las métricas utilizadas

## Limitaciones actuales

Las métricas implementadas no deben interpretarse como una medida directa de la calidad general de una producción de IA.

Entre las principales limitaciones se encuentran:

- la evaluación estructural utiliza actualmente una comparación posicional simple
- la evaluación de contenido actual es textual y no semántica
- el texto se normaliza para realizar las comparaciones textuales
- el análisis semántico todavía no forma parte de la evaluación
- el umbral utilizado para el fuzzy matching es un valor heurístico inicial y todavía no fue validado
- la corrección humana funciona como referencia para las comparaciones, pero los criterios utilizados todavía deben contrastarse con bibliografía, proyectos existentes y los resultados obtenidos sobre el propio conjunto de datos

## Proyección

A futuro, este trabajo se enmarca en una plataforma integral para la generación, revisión, evaluación y publicación de textos alternativos:

```text
captura del material
        ↓
generación automática mediante IA
        ↓
revisión y corrección humana
        ↓
evaluación
        ↓
generación del contenido para publicación
        ↓
generación del código QR
        ↓
preparación para publicación e impresión
```

Este proyecto se concentra en la etapa de evaluación.

## Inspección de `Document`

El constructor de `Document` transforma cada archivo preprocesado en una representación con:

- `structure`: secuencia ordenada utilizada principalmente por la evaluación estructural
- `content`: colecciones utilizadas por las evaluaciones de contenido

Para inspeccionar un par real:

```shell
./scripts/inspect_build_document.sh 01
```

## Documentación

La documentación técnica del pipeline se encuentra en:

```text
docs/pipeline.md
```