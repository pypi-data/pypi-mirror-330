import click
from python_project_manager.run_command import run_command

# Pip commands
@click.command()
@click.option('--help', '-h', is_flag=True) # Allows '--help' to be passed as an argument
def list(help) -> None:
    '''
    Uses pip's 'list' command
    '''
    if help:
        run_command(f'pip list --help', use_venv=True)
    run_command('pip list', use_venv=True)
