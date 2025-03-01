![CocoIndex](https://github.com/user-attachments/assets/2002d260-65f3-47a2-ab09-4cfacbe84835)

[![CI](https://github.com/cocoIndex/cocoindex/actions/workflows/CI.yml/badge.svg?event=push)](https://github.com/cocoIndex/cocoindex/actions/workflows/CI.yml)
[![release](https://github.com/cocoIndex/cocoindex/actions/workflows/release.yml/badge.svg?event=push)](https://github.com/cocoIndex/cocoindex/actions/workflows/release.yml)
[![docs](https://github.com/cocoIndex/cocoindex/actions/workflows/docs.yml/badge.svg?event=push)](https://github.com/cocoIndex/cocoindex/actions/workflows/docs.yml)

# CocoIndex

With CocoIndex, users declare the transformation, CocoIndex creates & maintains an index, and keeps the derived index up to date based on source update, with minimal computation and changes.


## Install Released CocoIndex Package

CocoIndex is a Python library. You can install via pip:

```bash
pip install cocoindex
```

## Setup Postgres

Currently, CocoIndex uses Postgres + pgvector for indexing pipeline metadata and the default indexing storage.
You need to setup a Postgres database with pgvector extension installed.

If you don't have your own Postgres database, or just want to try CocoIndex quickly, you can bring up a Postgres database using docker compose:

-   Make sure Docker Compose is installed: [docs](https://docs.docker.com/compose/install/)

-   Start a Postgres SQL database for cocoindex:

    ```bash
    docker compose -f dev/postgres.yaml up -d
    ```

## Try Examples

Go to the `examples` directory to try out with any of the examples, following instructions under specific example directory.
