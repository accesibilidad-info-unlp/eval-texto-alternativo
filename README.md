# Evaluación de textos alternativos

Proyecto para evaluar producciones de texto alternativo generadas mediante inteligencia artificial y posteriormente revisadas y corregidas por una persona.

El proyecto surge como parte de la experiencia de desarrollo de una plataforma de textos alternativos para materiales visuales educativos. 

Como etapa inicial se trabajó con una actividad del TIVU 2026 y se generó y evaluó las producciones automáticas por un humano, utilizando 53 archivos.

## Objetivo

El proyecto busca obtener mediciones sobre dos aspectos de las producciones generadas por IA:

* **Estructura:** grado de correspondencia con la estructura estandarizada definida para la plataforma
* **Contenido:** fidelidad y certeza de la información transcrita respecto del material visual original

La evaluación se encuentra en una etapa inicial y se desarrolla de manera iterativa a partir de la experiencia, la identificación de errores y la mejora de los criterios de evaluación.

## Origen de la estructura

La estructura utilizada por la plataforma no fue proporcionada inicialmente a la IA.

Durante una primera experiencia se analizaron las producciones generadas automáticamente y se identificaron elementos que resultaban útiles junto con otros que requerían corrección o unificación. A partir de esa experiencia se definió y documentó una estructura estandarizada para los textos publicados en la plataforma.

Posteriormente, este criterio se replicó en la revisión de los restantes documentos.

La estructura estandarizada utiliza:

* H1 para el título del contenido
* H2 para secciones de orientación
* Corchetes para indicar contexto, ubicación o agrupación dentro del material original
* Elementos textuales y párrafos para organizar el contenido de cada sección

Esta estructura está documentada en la Plataforma de textos alternativos (link).

## Datos de evaluación

El conjunto actual contiene 53 pares de documentos:

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

La revisión humana se realiza contrastando la producción automática con la imagen original del material. Esto permite utilizar las versiones humanas como referencia para las evaluaciones actuales.

## Pipeline

El procesamiento se organiza en etapas:

```text
datos
  ↓
preprocesamiento
  ↓
parseo
  ↓
evaluación
  ├── estructura
  └── contenido
  ↓
resultados
```

## Evaluadores

Por el momento solo 1. (A completar)

### Evaluación estructural

Compara la estructura producida por la IA con la estructura presente en la versión humana estandarizada.

Entre los elementos considerados se encuentran:

* secciones de orientación
* landmarks o referencias espaciales
* etiquetas organizativas
* párrafos
* listas
* orden de las secciones

El evaluador estructural se encuentra implementado y será refactorizado para mejorar su legibilidad, semántica y capacidad de extensión.

### Evaluación de contenido

La evaluación de contenido se incorpora para analizar la fidelidad y certeza de la información producida automáticamente.

(La metodología y las métricas concretas de esta evaluación se encuentran en desarrollo).

## Resultados

Los resultados de las evaluaciones se generan en formatos destinados tanto al análisis como a su futura visualización.

```text
outputs/
├── comparison.json
├── comparison.csv
└── summary.json
```

(La visualización mediante Eleventy se encuentra en desarrollo)

## Estado del proyecto

El proyecto se encuentra en una etapa de desarrollo iterativo.

El trabajo actual se concentra en:

1. refactorizar y consolidar la evaluación estructural
2. implementar la evaluación de contenido
3. validar las mediciones obtenidas sobre los 53 documentos
4. presentar y analizar los resultados

Posteriormente, se incorporará bibliografía y se contrastará la metodología utilizada con trabajos y herramientas existentes de evaluación de sistemas de inteligencia artificial.

## Proyección

A futuro, este trabajo se enmarca en el desarrollo de una plataforma integral para la generación, evaluación y publicación de textos alternativos.

La visión general contempla un flujo completo que integra todas las etapas del proceso:

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

Este proyecto se concentra actualmente en la etapa de evaluación, como parte de un sistema más amplio que busca articular de manera continua la generación, la validación y la publicación de textos alternativos.

## Inspección del parser

El parser transforma cada archivo Markdown preprocesado en un objeto `Document`.
Este objeto contiene dos representaciones del documento:

- `structure`: secuencia ordenada de elementos utilizada por la evaluación estructural
- `content`: colecciones de contenido utilizadas por la evaluación de contenido

Para inspeccionar el resultado sobre un par real:

```shell
./scripts/inspect_parse.sh 01