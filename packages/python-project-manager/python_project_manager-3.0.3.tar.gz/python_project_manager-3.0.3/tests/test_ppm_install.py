import os
import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_install import install
from python_project_manager.run_command import command_context
from tests.helper import working_directory
from python_project_manager.venv_helper import _VENV_SITE_PACKAGES

class TestPpmInstall(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_install(self):
        with command_context(is_silent=True):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(install, ['requests'], catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            packages.sort() # Guarantee order
            packages = '\n'.join(packages)
            requirement_file_string = ''
            with open('requirements.txt', 'r') as file:
                requirement_file_string = file.read()

            # Run tests
            self.assertEqual(packages,
'''certifi
certifi-2024.8.30.dist-info
charset_normalizer
charset_normalizer-3.3.2.dist-info
idna
idna-3.10.dist-info
pip
pip-24.2.dist-info
requests
requests-2.32.3.dist-info
urllib3
urllib3-2.2.3.dist-info''')
            self.assertEqual(requirement_file_string,
'''certifi~=2024.8.30
charset_normalizer~=3.3.2
idna~=3.10
requests~=2.32.3
urllib3~=2.2.3
''')

    @working_directory(cwd='tests/__cached__')
    def test_ppm_install_file(self):
        with command_context(is_silent=True):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])

            # Addlines to the requirements file
            with open('requirements.txt', 'w') as file:
                file.write('requests~=2.32.3\n')

            runner.invoke(install, catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            packages.sort() # Guarantee order
            packages = '\n'.join(packages)

            # Run tests
            self.assertEqual(packages,
'''certifi
certifi-2024.8.30.dist-info
charset_normalizer
charset_normalizer-3.3.2.dist-info
idna
idna-3.10.dist-info
pip
pip-24.2.dist-info
requests
requests-2.32.3.dist-info
urllib3
urllib3-2.2.3.dist-info''')

    @working_directory(cwd='tests/__cached__')
    def test_ppm_install_dev(self):
        with command_context(is_silent=True):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(install, ['requests', '--dev'], catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            packages.sort() # Guarantee order
            packages = '\n'.join(packages)
            requirement_file_string = ''
            with open('requirements-dev.txt', 'r') as file:
                requirement_file_string = file.read()

            # Run tests
            self.assertEqual(packages,
'''certifi
certifi-2024.8.30.dist-info
charset_normalizer
charset_normalizer-3.3.2.dist-info
idna
idna-3.10.dist-info
pip
pip-24.2.dist-info
requests
requests-2.32.3.dist-info
urllib3
urllib3-2.2.3.dist-info''')
            self.assertEqual(requirement_file_string,
'''certifi~=2024.8.30
charset_normalizer~=3.3.2
idna~=3.10
requests~=2.32.3
urllib3~=2.2.3
''')

    @working_directory(cwd='tests/__cached__')
    def test_ppm_install_dev_file(self):
        with command_context(is_silent=True):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])

            # Addlines to the requirements file
            with open('requirements-dev.txt', 'w') as file:
                file.write('requests~=2.32.3\n')

            runner.invoke(install, catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            packages.sort() # Guarantee order
            packages = '\n'.join(packages)

            # Run tests
            self.assertEqual(packages,
'''certifi
certifi-2024.8.30.dist-info
charset_normalizer
charset_normalizer-3.3.2.dist-info
idna
idna-3.10.dist-info
pip
pip-24.2.dist-info
requests
requests-2.32.3.dist-info
urllib3
urllib3-2.2.3.dist-info''')
        