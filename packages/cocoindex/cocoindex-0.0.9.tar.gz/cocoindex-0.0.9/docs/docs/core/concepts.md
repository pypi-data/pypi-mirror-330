---
title: Concepts
description: Basic CocoIndex concepts
---

# CocoIndex Concepts

An **index** is a collection of data stored in a way that is easy for retrieval.

CocoIndex is an ETL framework for building indexes from specified data sources, a.k.a. indexing. It also offers utilities for users to retrieve data from the indexes.

## Indexing Flow

An indexing flow extracts data from speicfied data sources, upon specified transformations, and puts the transformed data into specified storage for later retrieval.

An indexing flow has two aspects: data and operations on data.

### Data

An indexing flow involves source data and transformed data (either as an intermediate result or the final result to be put into storage). All data within the indexing flow has **schema** determined at flow definition time.

Each piece of data has a **data type**, falling into one of the following categories:

*   Basic type

    | Type                        | Representation in Python |
    |-----------------------------|--------------------------|
    | bytes                       | `bytes`                  |
    | str                         | `str`                    |
    | bool                        | `bool`                   |
    | int64                       | `int`                    |
    | float32                     | `float`                  |
    | float64                     | `float`                  |
    | range                       | `tuple[int, int]`        |
    | json                        | `Any`                    |
    | vector(*type*, *dimension*) | `list[type]`             |


*   Composite type
    *   Struct: a collection of **fields**, each with a name and a type.
    *   Table: a collection of rows, each of which is a struct with specified schema.

An indexing flow always has a top-level struct, containing all data within and managed by the flow.

### Operations

An **operation** in an indexing flow defines a step in the flow.

*   **Action**, which defines the behavior of the operation, e.g. *import*, *transform*, *for each*, *collect* and *export*.
    See [Flow Definition](flow_def) for more details for each action.

*   **Operation Spec**, which describes the specific behavior of certain actions, e.g. a source to import from, a function describing the transformation behavior, a storage to export to as an index. It's not needed for some actions like "for each row" and "collect".
    *   Each operation spec has a **operation type**, e.g. `LocalFile` for data source, `SplitRecursively` for function, `Postgres` for storage.
    *   CocoIndex framework maintains a set of supported operation types. Users can also implement their own.

### Example

For the example shown in the [Quickstart](../getting_started/quickstart) section, the indexing flow is as follows:

![Flow Example](flow_example.svg)

This creates the following data for the indexing flow:

*   The `Localfile` source creates a `documents` field at the top level, with `filename` (key) and `content` sub fields.
*   A "for each" action works on each document, with the following transformations:
    *   The `SplitRecursively` function splits content into chunks, adds a `chunks` field into the current scope (each document), with `location` (key) and `text` sub fields.
    *   A "collect" action works on each chunk, with the following transformations:
        *   The `SentenceTransformerEmbed` function embeds the chunk into a vector space, adding a `embedding` field into the current scope (each chunk).

This shows schema and example data for the indexing flow:

![Data Example](data_example.svg)

### Life Cycle of an Indexing Flow

An indexing flow, once set up, maintains a long-lived relationship between source data and indexes. This means:

1. The indexes created by the flow remain available for querying at any time
2. When source data changes, the indexes are automatically updated to reflect those changes
3. CocoIndex intelligently manages these updates by:
   - Determining which parts of the index need to be recomputed
   - Reusing existing computations where possible
   - Only reprocessing the minimum necessary data

You can think of an indexing flow similar to formulas in a spreadsheet:

- In a spreadsheet, you define formulas that transform input cells into output cells
- When input values change, the spreadsheet automatically recalculates affected outputs
- You focus on defining the transformation logic, not managing updates

CocoIndex works the same way, but with more powerful capabilities:

- Instead of cells, you work with rich data structures like multi-layer tables
- Instead of simple cell formulas, you have operations like "for each" and "collect" 
- But the core idea is the same - you define how to transform source data into indexes, and CocoIndex handles keeping those indexes up-to-date automatically

This means when writing your flow operations, you can treat source data as if it were static - focusing purely on defining the transformation logic. CocoIndex takes care of maintaining the dynamic relationship between sources and indexes behind the scenes.

## Retrieval

There are two ways to retrieve data from indexes built by an indexing flow:

*   Query the underlying index storage directly for maximum flexibility.
*   Use CocoIndex *query handlers* for a more convenient experience with built-in tooling support (e.g. CocoInsight) to understand query performance against the index.

Query handlers are tied to specific indexing flows. They accept query inputs, transform them by defined operations, and retrieve matching data from the index storage that was created by the flow.