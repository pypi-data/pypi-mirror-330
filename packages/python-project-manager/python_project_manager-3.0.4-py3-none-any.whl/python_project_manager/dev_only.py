import click
import os

@click.command()
@click.argument('version', type=str, default=None, required=False)
def fix(version):
    '''
    For development purposes only. Force re-install the package with the specified version or newest version if not specified.
    '''
    if version is None:
        os.system('pip install --force-reinstall python-project-manager')
    else:
        os.system(f'pip install --force-reinstall python-project-manager=={version}')

if __name__ == '__main__':
    print('This script is for development purposes only. It is not meant to be used in production.')