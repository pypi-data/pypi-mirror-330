import click

@click.group()
def cli():
    pass

# Commands
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_run import run
from python_project_manager.ppm_commands.ppm_version import version
from python_project_manager.ppm_commands.ppm_install import install
from python_project_manager.ppm_commands.ppm_list import list
from python_project_manager.ppm_commands.ppm_venv import venv

cli.add_command(init)
cli.add_command(run)
cli.add_command(version)
cli.add_command(install)
cli.add_command(list)
cli.add_command(venv)