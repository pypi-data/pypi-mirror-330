import click
import json
from pydantic import BaseModel

from .types import Actor, Activity, Object


@click.group
def main(): ...


def to_json_schema(model: BaseModel, filename: str):
    schema = model.model_json_schema()

    with open(filename, "w") as f:
        json.dump(schema, f, indent=2)


@main.command()
@click.option("--path", default="docs/schemas/")
def schemas(path):
    to_json_schema(Actor, f"{path}/actor.json")  # type: ignore
    to_json_schema(Activity, f"{path}/activity.json")  # type: ignore
    to_json_schema(Object, f"{path}/object.json")  # type: ignore


if __name__ == "__main__":
    main()
