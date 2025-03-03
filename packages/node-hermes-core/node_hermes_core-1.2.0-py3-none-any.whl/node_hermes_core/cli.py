import time
from typing import List

import click
from node_hermes_core.nodes.depedency import HermesDependencies
from node_hermes_core.loader import load_modules


@click.group()
def cli():
    pass


@cli.command()
@click.option("--output", "-o", required=True, help="Output schema file")
@click.option("--packages", "-p", multiple=True, help="Packages to load", default=None)
@click.option("--config", "-c", help="Config file", default=None)
def schema(output: str, packages: List[str] | None, config: str | None):
    if config:
        modules = HermesDependencies.import_from_yaml(config)
    elif packages:
        modules = load_modules(packages)
    else:
        raise ValueError("Either --config or --packages must be specified")

    print("Loaded modules:")
    for module in modules:
        print(f" - {module.__name__}")

    # Reload the model to add the new components
    from node_hermes_core.nodes.root_nodes import HermesConfig

    with open(output, "w") as schema_file:
        schema_file.write(HermesConfig.get_schema_json())


@cli.command()
@click.argument("config_path", type=str)
def run(config_path: str):
    # Load the required modules in order to be able to parse the full configuration
    HermesDependencies.import_from_yaml(config_path)

    # Reload the configuration
    import logging

    from node_hermes_core.nodes.root_nodes import HermesConfig

    logging.basicConfig(level=logging.DEBUG)
    config = HermesConfig.from_yaml(config_path)
    root_node = config.get_root_node()
    root_node.attempt_init()

    while True:
        time.sleep(1)


def generate_schema():
    cli()


if __name__ == "__main__":
    cli()
