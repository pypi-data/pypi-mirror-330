import re
import click
import os
from python_project_manager.config import Config
from python_project_manager.run_command import run_command
from python_project_manager.venv_helper import _VENV_SITE_PACKAGES, is_venv_installed

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--dev', '-d', is_flag=True, help='Adds the dependencies to the `requirements-dev.txt` instead of `requirements.txt`') # Add the package to the dev requirements
@click.option('--not_required', '-n', is_flag=True, help='Dependencies are not added to either `requirements.txt` or `requirements-dev.txt`')
def install(args, dev, not_required) -> None:
    '''
    Uses pip to install packages in the virtual environment
    Args will be passed directly to pip
    '''
    # Stringify the arguments
    pip_command = f'pip install {" ".join(args)}'.strip()

    # Install pip
    if pip_command == 'pip install pip':
        run_command(f'python -m ensurepip', use_venv=True)
        return
    
    # Create Virtual Environment if it does not exist
    if not is_venv_installed():
        run_command('python -m venv venv', use_venv=False)

    # Get the extra index url and trusted host
    extra_index_url = ' '.join([f'--extra-index-url {url}' for url in Config.get('pip.extra_index_url', [])])
    trusted_host = ' '.join([f'--trusted-host {host}' for host in Config.get('pip.trusted_host', [])])

    # If no arguments are passed, install the requirements
    if pip_command == f'pip install':
        run_command(f'pip install -r requirements.txt -r requirements-dev.txt {extra_index_url} {trusted_host}'.strip(), use_venv=True)
        return

    # New packages
    pre_packages = get_packages()
    run_command(f'{pip_command} {extra_index_url} {trusted_host}', use_venv=True)
    post_packages = get_packages()
    if not not_required:
        add_packages_to_requirements(get_new_packages(pre_packages, post_packages), dev)

def get_packages() -> str:
    '''
    Get the packages in the site-packages directory
    '''
    packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f)) and f.endswith('.dist-info')]
    # Remove 'pip' (ex. 'pip-24.2.dist-info')
    pip_regex = r'^pip-.+\.dist-info$'
    packages = [package for package in packages if not re.match(pip_regex, package)]
    return packages

def get_new_packages(pre_packages: list, post_packages: list) -> dict:
    '''
    Takes two lists of packages and returns a dictionary of only the new packages
    '''
    new_packages = []
    for package in post_packages:
        if package not in pre_packages:
            new_packages.append(package)
    package_dict = {}
    encode_regex = r'^(?P<name>.+?)-(?P<version>[\d|\.]+)\.dist-info$'
    for package in new_packages:
        match = re.match(encode_regex, package)
        if match:
            package_dict[match.group('name')] = f'{match.group("name")}~={match.group("version")}'
    return package_dict

def get_requirements_packages(use_dev: bool) -> dict:
    '''
    Creates a dictionary of the packages in the requirements file
    '''
    target_file = 'requirements-dev.txt' if use_dev else 'requirements.txt'
    with open(target_file, 'r') as file:
        packages = file.readlines()
    
    package_dict = {}
    encode_regex = r'^(?P<name>.+?)(~=|==|!=>=|<=|>|<).+$'
    for package in packages:
        match = re.match(encode_regex, package)
        if match:
            package_dict[match.group('name')] = package.strip()
    return package_dict

def add_packages_to_requirements(new_packages: dict, dev: bool):
    '''
    Adds the new packages to the requirements file
    '''
    target_file = 'requirements-dev.txt' if dev else 'requirements.txt'
    requirements_packages = get_requirements_packages(dev)
    # loop through the new packages and add them to the requirements file if they are not already there
    for name, version in new_packages.items():
        if name not in requirements_packages:
            requirements_packages[name] = version
    # write the new requirements to the file
    with open(target_file, 'w') as file:
        for package in requirements_packages.values():
            file.write(f'{package}\n')