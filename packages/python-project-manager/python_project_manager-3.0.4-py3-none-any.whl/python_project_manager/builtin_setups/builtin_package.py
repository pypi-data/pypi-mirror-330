import os
import click
import python_project_manager

@click.command()
@click.argument('project_name', type=str, required=True)
def package_setup(project_name):
    if len(os.listdir(os.getcwd())) != 0:
        print('Project already initialized')
        return
    
    _src_path = project_name
    _test_path = 'tests'
    _version = '0.0.0b1'
    
    initializer = python_project_manager.Initializer()
    initializer.AddConfigValue('project_name', project_name)
    initializer.AddConfigValue('src_dir', _src_path)
    initializer.AddConfigValue('test_dir', _test_path)
    initializer.AddConfigValue('include_paths', [_src_path])
    initializer.AddConfigValue('version', _version)
    initializer.AddConfigValue('twine.wheel', pep508_sanitizer(project_name))
    initializer.AddConfigValue('twine.username', r'%env:pypi_username%')
    initializer.AddConfigValue('twine.password', r'%env:pypi_password%')
    initializer.AddConfigValue('scripts.publish', 'ppm run _build_and_publish')
    initializer.AddConfigValue('scripts.install:local', 'ppm version inc -t && ppm run _build && ppm run _install --local')
    initializer.AddConfigValue('scripts.uninstall:local', 'ppm run _uninstall --local')
    initializer.AddConfigValue('scripts.playground', f'python -m %test_dir%.playground')
    initializer.AddConfigValue('scripts._rm_dist', 'del /Q dist')
    initializer.AddConfigValue('scripts._build', 'ppm run _rm_dist && ppm run _sync -p && python -m build')
    initializer.AddConfigValue('scripts._install', 'python -m pip install dist/%twine.wheel%-%version%-py3-none-any.whl --force-reinstall')
    initializer.AddConfigValue('scripts._uninstall', 'python -m pip uninstall dist/%twine.wheel%-%version%-py3-none-any.whl -y')
    initializer.AddConfigValue('scripts._sync', 'dev_scripts/sync.py')
    initializer.AddConfigValue('scripts._build_and_publish', 'ppm run _build && ppm run _publish')
    initializer.AddConfigValue('scripts._publish', 'twine upload -u %twine.username% -p %twine.password% -r testpypi dist/*')
    initializer.AddFolder(_src_path)
    initializer.AddFolder(_test_path)
    initializer.AddFolder('dev_scripts')
    initializer.AddFile(f'{_src_path}/__init__.py', '')
    initializer.AddFile(f'{_src_path}/template.py',
'''
def template():
    print('Hello World')
''')
    initializer.AddFile(f'{_test_path}/playground.py',
'''
from template import template
template()
''')
    initializer.AddFile('dev_scripts/sync.py',
r'''
import re
import python_project_manager

version = python_project_manager.Config.get('version')
if version is None:
    raise ValueError('Version not found in \'.proj.config\'')

toml_path = 'pyproject.toml'
with open(toml_path, 'r') as file:
    toml = file.read()
version_regex = r'version = ".*?"'
toml = re.sub(version_regex, f'version = "{version}"', toml)
with open(toml_path, 'w') as file:
    file.write(toml)
''')
    initializer.AddFile('pyproject.toml',
f'''
[build-system]
requires = [ "setuptools>=61.0",]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
description = "A Python package."
authors = []
readme = "README.md"
keywords = []
version = "0.0.0b1"
dynamic = [ "dependencies",]

[tool.setuptools]
packages = ["{pep508_sanitizer(project_name)}"]

[tool.setuptools.dynamic.dependencies]
file = [ "requirements.txt",]

[tool.setuptools.packages.find]
include = ["{project_name}*"]
''')
    initializer.AddFile('README.md',
f'''
# {project_name}

A Python package.
''')
    initializer.AddFile('.env',
'''
pypi_username=__token__
pypi_password=pypi-AgENdGVz...
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
''')
    
    initializer.Initialize()
    python_project_manager.RunCommand('python -m venv venv', use_venv=False)
    # python_project_manager.RunCommand('ppm install python-dotenv', use_venv=True)
    python_project_manager.RunCommand('ppm install build==1.2.2 twine==5.1.1 -d', use_venv=True)
    print(f'Project {project_name} created')

def pep508_sanitizer(value: str) -> str:
    return value.replace('-', '_')