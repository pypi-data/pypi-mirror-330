import argparse
import json
from json import JSONDecodeError
from typing import Optional

import yaml
from schemax import collect_schema_data
from schemax._generator import MainGenerator


def generate(file: str, base_url: Optional[str] = None, humanize: bool = False) -> None:
    try:
        with open(file, "r") as f:
            print("Generating schemas and interfaces from given OpenApi...")
            if f.name.endswith(".json"):
                schema_data = collect_schema_data(json.load(f))
            elif f.name.endswith((".yaml", ".yml")):
                schema_data = collect_schema_data(yaml.load(f, yaml.FullLoader))
            else:
                print(f"'{f.name}' type is not .json or .yaml file")
                exit(1)

            generator = MainGenerator(schema_data, base_url, humanize)
            generator.all()
            print("Successfully generated")
    except FileNotFoundError:
        print(f"File '{file}' doesn't exist")
        exit(1)
    except JSONDecodeError:
        print(f"File '{f.name}' doesn't contain proper JSON")
        exit(1)


def command() -> None:
    parser = argparse.ArgumentParser(description="vedro openapi basic tests generator")
    subparsers = parser.add_subparsers(help="Available commands", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate Tests")
    generate_parser.add_argument(
        "openapi_spec_path", type=str, help="Path to OpenAPI specification"
    )
    generate_parser.add_argument(
        "--humanize", type=bool, help="Make generated names more human-friendly", default=False
    )
    generate_parser.add_argument("--base_url", type=str, help="Basic url for tests", default="")
    generate_parser.set_defaults(command=generate)

    args = parser.parse_args()
    args.command(args.openapi_spec_path, args.base_url, args.humanize)


if __name__ == "__main__":
    command()
