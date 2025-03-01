import os
import shutil
import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_venv import venv
from python_project_manager.run_command import command_context
from python_project_manager.venv_helper import _VENV_SITE_PACKAGES, _VENV_PATH
from tests.helper import working_directory

class TestPpmVenv(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_venv(self):
        with command_context(is_silent=True):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            with open('requirements.txt', 'w') as file:
                file.write('build~=1.2.1\n')
            with open('requirements-dev.txt', 'w') as file:
                file.write('certifi~=2024.2.2\n')
            shutil.rmtree(_VENV_PATH, ignore_errors=True)
            
            runner.invoke(venv, catch_exceptions=False, input='y\n') # colorama~=0.4.6
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            packages.sort()
            packages = '\n'.join(packages)
            self.assertEqual(packages, '''build
build-1.2.2.dist-info
certifi
certifi-2024.2.2.dist-info
colorama
colorama-0.4.6.dist-info
packaging
packaging-24.1.dist-info
pip
pip-24.2.dist-info
pyproject_hooks
pyproject_hooks-1.1.0.dist-info''')