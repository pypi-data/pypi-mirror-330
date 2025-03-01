import time
import re
from python_project_manager.config import Config
import click

@click.command()
@click.argument('action', type=click.Choice(['inc', 'show', 'set']), required=True, default='show')
@click.option('--major', '-M', type=int, default=None, help='Major version')
@click.option('--minor', '-m', type=int, default=None, help='Minor version')
@click.option('--patch', '-p', type=int, default=None, help='Patch version')
@click.option('--alpha', '-a', type=int, default=None, help='Alpha version')
@click.option('--beta', '-b', type=int, default=None, help='Beta version')
@click.option('--rc', '-r', type=int, default=None, help='Release candidate version')
@click.option('--local', '-l', type=str, default=None, help='Local version')
@click.option('--timestamp', '-t', is_flag=True, help='Preset: ad the current timestamp to the local version')
def version(action, major, minor, patch, alpha, beta, rc, local, timestamp) -> None:
    '''
    <action>: The action to perform on the project version. ['inc', 'show', 'set'] default: 'show'
    '''
    version = Config.get('version')
    if action == 'show':
        print(version)
        return
    
    # Raise error if -l or any preset option is used
    if local and (timestamp):
        print('\033[91mError: -l and -t cannot be used together\033[0m')
        return
    
    if timestamp:
        local = time.strftime('%Y%m%d%H%M%S')

    if action == 'inc':
        new_version = inc_version(version, major, minor, patch, alpha, beta, rc, local)
    elif action == 'set':
        new_version = set_version(version, major, minor, patch, alpha, beta, rc, local)
    else:
        print(f'\033[91mError: Action \'{action}\' is not implemented yet\033[0m')
        return

    if new_version is None:
        return
    
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(f'Version updated from {YELLOW+version+RESET} to {YELLOW+new_version+RESET}')
    Config.set('version', new_version)
    Config.save()

def inc_version(version: str, major: int|None, minor: int|None, patch: int|None, alpha: int|None, beta: int|None, rc: int|None, local: str|None) -> str:
    # raise error if more than one version part is incremented
    _n = len([n for n in [major, minor, patch, alpha, beta, rc, local] if n is not None])
    if _n > 1:
        print('\033[91mError: Only one version part can be incremented at a time\033[0m')
        return
    elif _n == 0:
        print('\033[91mError: No version part is specified to increment\033[0m')
        return

    def _inc(version_dict: dict, major: int|None, minor: int|None, patch: int|None, alpha: int|None, beta: int|None, rc: int|None, local: str|None) -> dict:
        if local is not None:
            version_dict['local'] = local
            return version_dict
        else: version_dict['local'] = None

        if alpha is not None or beta is not None or rc is not None:
            target_pretype: str
            amount: int
            if alpha is not None:
                target_pretype = 'a'
                amount = alpha
            elif beta is not None:
                target_pretype = 'b'
                amount = beta
            elif rc is not None:
                target_pretype = 'rc'
                amount = rc
                
            if version_dict['pretype'] == target_pretype:
                version_dict['preval'] += amount
            else:
                version_dict['pretype'] = target_pretype
                version_dict['preval'] = amount

            return version_dict
        else:
            version_dict['pretype'] = None
            version_dict['preval'] = None

        if patch is not None:
            version_dict['patch'] += patch
            return version_dict
        else: version_dict['patch'] = 0

        if minor is not None:
            version_dict['minor'] += minor
            return version_dict
        else: version_dict['minor'] = 0

        if major is not None:
            version_dict['major'] += major
            return version_dict
        else: version_dict['major'] = 0

        return version_dict

    version_dict = parse_version(version)
    version_dict = _inc(version_dict, major, minor, patch, alpha, beta, rc, local)
    return format_version(version_dict)

def set_version(version: str, major: int|None, minor: int|None, patch: int|None, alpha: int|None, beta: int|None, rc: int|None, local: str|None) -> str:
    # Raise error if more than one aplha, beta, rc is set
    _n = len([n for n in [alpha, beta, rc] if n is not None])
    if _n > 1:
        print('\033[91mError: Only one pre-release type can be set at a time\033[0m')
        return

    version_dict = parse_version(version)
    if major is not None: version_dict['major'] = major
    if minor is not None: version_dict['minor'] = minor
    if patch is not None: version_dict['patch'] = patch
    if alpha is not None:
        version_dict['pretype'] = 'a'
        version_dict['preval'] = alpha
    if beta is not None:
        version_dict['pretype'] = 'b'
        version_dict['preval'] = beta
    if rc is not None:
        version_dict['pretype'] = 'rc'
        version_dict['preval'] = rc
    if local is not None: version_dict['local'] = local

    return format_version(version_dict)

def parse_version(version: str) -> dict:
    '''
    Parse the version string into a dictionary
    '''
    regex = r"^(?P<major>\d*)?.(?P<minor>\d*)?.(?P<patch>\d*)?(?P<pretype>a|b|rc)?(?P<preval>\d*)?(\+(?P<local>[a-zA-Z0-9]*)?)?"
    matches = re.match(regex, version)
    if matches:
        version_dict = matches.groupdict()
        for key in ['major', 'minor', 'patch', 'preval']:
            if version_dict[key]:
                version_dict[key] = int(version_dict[key])
        return version_dict
    
def format_version(version_dict: dict) -> str:
    '''
    Format the version dictionary into a string
    '''
    version = f"{version_dict['major']}.{version_dict['minor']}.{version_dict['patch']}"
    if version_dict['pretype']:
        version += f"{version_dict['pretype']}{version_dict['preval']}"
    if version_dict['local']:
        version += f"+{version_dict['local']}"
    return version