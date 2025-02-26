import os

import click
from click import Abort

from wikimine.db import connect
from wikimine.tasks.unpack import split_wikidata_dump
from wikimine.tasks.wikidata_dump import init_wikidata, add_wikidata_dump_folder
from wikimine.tasks.wikidata_index import build_wikidata_index


@click.group()
def cli():
    """
        a cli app that load wikidata into sqlite.
        Steps:
        1. download the wikidata dump.
        2. use split command the wikidata dump into parts.
        2. use import command import the split wikidata dump.
        2. use index command build index.
    """
    pass


def ensure_exist(file_path):
    if not os.path.exists(file_path):
        click.secho(f'{file_path} do not exists', fg='red', bold=True)
        raise Abort()


def ensure_is_file(file_path):
    ensure_exist(file_path)
    if not os.path.isfile(file_path):
        click.secho(f'{file_path} is not a file', fg='red', bold=True)
        raise Abort()


def ensure_is_folder(file_path):
    ensure_exist(file_path)
    if not os.path.isdir(file_path):
        click.secho(f'{file_path} is not a folder', fg='red', bold=True)
        raise Abort()


@click.command('index')
@click.argument("db_path")
def index_cli(db_path):
    """build db index"""
    ensure_is_file(db_path)
    build_wikidata_index(db_path)


@click.command('import')
@click.argument("db_path")
@click.argument("dump_folder_path")
def import_cli(db_path, dump_folder_path):
    """process wikidata dump and load its content into sqlite"""
    ensure_is_file(db_path)
    ensure_is_folder(dump_folder_path)
    connect(db_path)
    init_wikidata()
    add_wikidata_dump_folder(dump_folder_path)


@click.command('split')
@click.argument("dump_path")
@click.argument("dump_folder_path")
@click.option("-b", "--batch", default=5000, type=int, help='size of batch')
@click.option("-s", "--stop_at", default=None, type=int, help='stop processing after this many items')
def split_cli(dump_path, dump_folder_path, batch, stop_at):
    """split wikidata dump for easier processing"""
    ensure_is_file(dump_path)
    ensure_is_folder(dump_folder_path)
    split_wikidata_dump(
        dump_path,
        dump_folder_path,
        batch_size=batch,
        stop_at=stop_at,
    )


# Add commands to the CLI group
cli.add_command(index_cli)
cli.add_command(import_cli)
cli.add_command(split_cli)

if __name__ == "__main__":
    cli()
