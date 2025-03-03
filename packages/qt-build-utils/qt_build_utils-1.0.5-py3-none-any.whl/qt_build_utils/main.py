import subprocess
from typing import List

import click

from .convert import convert_ui
from .path_manager import manager


@click.group()
def cli():
    pass


@cli.command()
@click.argument("sources", type=click.Path(exists=True), required=True, nargs=-1)
@click.option("--inplace", "-i", is_flag=True, help="Convert the files in place")
@click.option("--target", "-t", help="Target directory for the converted files")
def convert(sources: List[str], inplace: bool, target: str | None):
    for source in sources:
        convert_ui(source, inplace, target)


# edit command
@cli.command()
@click.argument("sources", type=click.Path(exists=True), required=True, nargs=-1)
def edit(sources: str):
    designer = manager.find_executable_variants(["pyside6-designer", "pyside2-designer"])

    subprocess.run(f"{designer} {sources}", shell=True)


if __name__ == "__main__":
    cli()
