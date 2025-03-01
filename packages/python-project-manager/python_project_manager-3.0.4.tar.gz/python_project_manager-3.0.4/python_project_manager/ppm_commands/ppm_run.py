import os
from python_project_manager.config import Config
import click
from python_project_manager.run_command import run_command

@click.command()
@click.argument('script_name', type=str)
@click.option('--local', '-l', is_flag=True, help='Run the script in the local environment NOT in the virtual environment')
@click.option('--python', '-p', is_flag=True, help='Run as a Python script or file')
def run(script_name, local, python) -> None:
    '''
    <script_name>: The name of the script located in the `scripts` section of the `.proj.config` file
    '''
    cli_command: str = Config.get(f'scripts.{script_name}')

    if not cli_command:
        print(f"Script '{script_name}' not found")
        return

    if python: # Run as a python script
        if os.path.isfile(cli_command):
            with open(cli_command, 'r') as file:
                py_script = file.read()
        else:
            py_script = cli_command

        exec(py_script)
        return

    run_command(cli_command, use_venv=not local)