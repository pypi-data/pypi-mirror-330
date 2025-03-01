import os
import click
import python_project_manager

@click.command()
@click.argument('project_name', type=str, required=True)
def exe_setup(project_name):
    if len(os.listdir(os.getcwd())) != 0:
        print('Project already initialized')
        return
    
    _src_path = 'src'
    _version = '0.0.0b1'
    
    initializer = python_project_manager.Initializer()
    initializer.AddConfigValue('project_name', project_name)
    initializer.AddConfigValue('src_dir', _src_path)
    initializer.AddConfigValue('include_paths', [_src_path])
    initializer.AddConfigValue('version', _version)
    initializer.AddConfigValue('scripts.start', r'python Application.py')
    initializer.AddConfigValue('scripts.build', r'ppm run __sync && ppm run __build')
    initializer.AddConfigValue('scripts.__sync', r'python dev_scripts/sync.py')
    initializer.AddConfigValue('scripts.__build', r'pyinstaller Application.py --noconfirm --clean --onefile --name %project_name%_v%version% --add-data %src_dir%/resources:.')
    initializer.AddFolder(f'{_src_path}/resources')
    initializer.AddFolder('dev_scripts')
    initializer.AddFile(f'Application.py',
'''
\'\'\'
    This file is the entry point of the application.

    It is responsible for setting up the file paths, loading the environment variables, and launching the application.

    Only handles exceptions that occur during the setup process all other exceptions should be handled by the application.

    The application should be launched by running this file.

    `resource` is the directory that contains the application files.

    `.app.env` is the environment file that contains required environment variables.
\'\'\'

import traceback
try:
    import os as _os
    import sys as _sys
    import ctypes as _ctypes
    from dotenv import load_dotenv as _load_dotenv
    from pathlib import Path as _Path
    import json as _json
    import base64 as _base64
    import hashlib as _hashlib
    from cryptography.fernet import Fernet as _Fernet, InvalidToken as _InvalidToken
    import platform as _platform

#region ApplicationSetup
    class Paths:
        ResourcePath: str
        LocalPath: str
        HiddenPath: str

        @staticmethod
        def GetResource(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the resource directory.
            \'\'\'
            return _os.path.join(Paths.ResourcePath, path)
        
        @staticmethod
        def GetLocal(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the user's local directory.
            \'\'\'
            return _os.path.join(Paths.LocalPath, path)
        
        @staticmethod
        def GetHidden(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the hidden directory.
            \'\'\'
            return _os.path.join(Paths.HiddenPath, path)

        @staticmethod
        def Open() -> None:
            \'\'\'
            Opens to the application's directory.
            \'\'\'
            _os.startfile(Paths.LocalPath)
        
        @staticmethod
        def Dump():
            for key in dir(Paths):
                _value = getattr(Paths, key)
                if key.startswith('__'): continue
                _type = type(_value).__name__
                if _type == 'module': continue
                print(f'\\033[93m{Paths.__name__}.{key}:\\033[0m \\033[94m{_type}\\033[0m = \\033[92m{_value}\\033[0m')

    class Secure:
        SecureFile = '.secure'

        @staticmethod
        def Get(key: str) -> str:
            \'\'\'
            Returns the value of a key in the secure file.
            \'\'\'
            return Secure.__load_secure().get(key)

        @staticmethod
        def Set(key: str, value: str) -> None:
            \'\'\'
            Sets the value of a key in the secure file.
            \'\'\'
            s = Secure.__load_secure()
            s[key] = value
            Secure.__save_secure(s)
        
        @staticmethod
        def __load_secure() -> dict:
            \'\'\'
            Loads the secure file.
            \'\'\'
            Paths.GetHidden(Secure.SecureFile)
            if not _os.path.exists(Paths.GetHidden(Secure.SecureFile)): return {}
            with open(Paths.GetHidden(Secure.SecureFile), 'r') as file:
                text = file.read()
                if text == '': return {}
                try:
                    text = _Fernet(Secure.__genkey()).decrypt(text.encode()).decode()
                except _InvalidToken:
                    #Print in red
                    print("\\033[91mIncorrect decryption key!\\nNo secure data will be loaded.\\033[0m")
                    return {}
                return _json.loads(text)
            
        @staticmethod
        def __save_secure(data: dict) -> None:
            \'\'\'
            Saves the secure file.
            \'\'\'
            with open(Paths.GetHidden(Secure.SecureFile), 'w') as file:
                text = _json.dumps(data, indent=4)
                text = _Fernet(Secure.__genkey()).encrypt(text.encode()).decode()
                file.write(text)

        @staticmethod
        def __genkey() -> str:
            \'\'\'
            Generates a key using the system's information.
            \'\'\'
            if _platform.system() == 'Windows':
                return _base64.urlsafe_b64encode(_hashlib.sha256(_os.popen("wmic csproduct get uuid").read().strip().split("\\n")[1].encode()).digest()).decode()
            else:
                raise Exception('Unsupported platform')

    # Pre .env load
    IsExecutable = hasattr(_sys, 'frozen')
    Paths.ResourcePath = _sys._MEIPASS if IsExecutable else _os.path.abspath('./src/resources')

    # Load .env
    _load_dotenv(Paths.GetResource('.env'))
    _load_dotenv(Paths.GetResource('.app.env'))
    Name: str | None = _os.environ.get('APP_NAME')
    Version:  str | None = _os.environ.get('APP_VERSION')
    __auto_retry: bool = _os.environ.get('APP_AUTO_RETRY', 'true').lower() == 'true'
    __env_errors = []
    if Name is None: __env_errors.append('APP_NAME')
    if Version is None: __env_errors.append('APP_VERSION')
    if len(__env_errors) > 0:
        raise Exception(f"Missing environment variables: {', '.join(__env_errors)}")

    # Post .env load
    __user_path = _os.path.join(_Path.home(), 'AppData\\\\Local') if IsExecutable else _os.path.abspath('./__Local__')
    Paths.LocalPath = _os.path.join(__user_path, Name)
    Paths.HiddenPath = _os.path.join(__user_path, Name, '.data')

    def __create_directory(path: str, hidden: bool):
        if not _os.path.exists(path):
            _os.makedirs(path)
            if hidden:
                _ctypes.windll.kernel32.SetFileAttributesW(path, 2)
    __create_directory(Paths.LocalPath, False)
    __create_directory(Paths.HiddenPath, True)
            

    def Dump():
        import Application
        # print each key(in yellow), type(in blue) and value(in green) in this format: key: type = value
        for key in dir(Application):
            _value = getattr(Application, key)
            if key.startswith('__'): continue
            _is_class = str(_value).startswith('<class ')
            _type = type(_value).__name__
            if _type == 'module': continue
            print(f'\\033[93m{key}:\\033[0m \\033[94m{_type}\\033[0m = \\033[92m{_value}\\033[0m')
            if _is_class and hasattr(_value, 'Dump'):
                try: _value.Dump()
                except: print(f'\\033[91mFailed to dump {key}!\\033[0m')
#endregion

#region ApplicationLauncher
    def __launch_application():
        from src.main import main
        while True:
            try:
                main()
                return True
            except Exception as e:
                print("\\n\\033[91mApplication crashed with error:\\033[0m")
                traceback.print_exc()
                if not __auto_retry:
                    input("Press Enter to exit...")
                    return False
                input("Press Enter to restart...")

    def __launcher_setup():
        try:
            print('\\033[92m' + Name + ' v' + Version + '\\033[0m')
            return __launch_application()
        except Exception as e:
            print("\\n\\033[91mLauncher failed to start application with error:\\033[0m")
            traceback.print_exc()
            input("Press Enter to exit...")
            return False

    if __name__ == '__main__':
        if __launcher_setup():
            input("\\n\\033[94mApplication exited successfully!\\033[0m\\nPress Enter to exit...")
#endregion
except Exception as e:
    print("\\n\\033[91mLauncher crashed with error:\\033[0m")
    traceback.print_exc()
    input("Press Enter to exit...")
''')
    initializer.AddFile(f'src\\resources\\.app.env',
f'''
APP_NAME={project_name} # Application Name
APP_VERSION={_version} # Application Version
APP_AUTO_RETRY=true # If the applicaion crashes, launcher will relaunch the application
''')
    initializer.AddFile(f'{_src_path}/main.py',
r'''
import Application

def main(): # DO NOT REMOVE THIS DEFINITION, IT IS USED BY THE LAUNCHER TO START THE APPLICATION
    print(f'Hello from {Application.Name} v{Application.Version}!')
    # print(Application.Paths.Open())
''')
    initializer.AddFile(f'dev_scripts/sync.py',
r'''
import json
import re
with open('.proj.config', 'r') as config:
    config_text = config.read()
    config_data = json.loads(config_text)
    config_version = config_data['version']
    print(config_version)
    env_text: str
    with open('src/resources/.app.env', 'r') as env:
        env_text = env.read()
        env_version_regex = r'(?P<a>^APP_VERSION=\s*)(?P<v>[^#]*?)(?P<b>\s*#.*?$|$)'
        env_text = re.sub(env_version_regex, r'\g<a>' + config_version + r'\g<b>', env_text, flags=re.MULTILINE)
        print(env_text)
    with open('src/resources/.app.env', 'w') as env:
        env.write(env_text)
''')
    initializer.AddFile('.gitignore',
'''
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
instance/
.webassets-cache
.scrapy
docs/_build/
.pybuilder/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.pdm.toml
.pdm-python
.pdm-build/
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
__Local__/
''')
    
    initializer.Initialize()
    python_project_manager.RunCommand('python -m venv venv', use_venv=False)
    python_project_manager.RunCommand('ppm install python-dotenv==1.0.1', use_venv=True)
    python_project_manager.RunCommand('ppm install pyinstaller==6.10.0 -d', use_venv=True)
    print(f'Project {project_name} created')