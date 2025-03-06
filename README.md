# LaKocie Dataset Repository

This repository is storing a tool/package that creates wet cat food **dataset** and a `ipynb` notebook containing in-depth analysis of dataset.


## Installation and usage

The package is built around project management and dependency tool by Astral.sh team - [uv](https://docs.astral.sh/uv/).


## migrations

```bash
# both commands from src/lakocie-dataset

# automatically migrate according to changes in schemas
$alembic revision --autogenerate -m "Initial migration"

# migrate and create tables
$alembic upgrade head
```
