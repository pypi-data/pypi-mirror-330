import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_version import version
from tests.helper import strip_color, working_directory

YELLOW_TEXT = '\033[93m'
RESET_TEXT = '\033[0m'

class TestPpmVersion(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_version_show(self):
        Config.load()
        runner = CliRunner()
        runner.invoke(init, ['test_project'])
        result = runner.invoke(version, catch_exceptions=False)
        self.assertEqual(result.output, '0.0.0b1\n')

    @working_directory(cwd='tests/__cached__')
    def test_ppm_version_inc(self):
        Config.load()
        runner = CliRunner()
        runner.invoke(init, ['test_project'])
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--local', 'thislocal'], catch_exceptions=False).output),
            f'Version updated from 0.0.0b1 to 0.0.0b1+thislocal\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--rc', '7'], catch_exceptions=False).output),
            f'Version updated from 0.0.0b1+thislocal to 0.0.0rc7\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--beta', '7'], catch_exceptions=False).output),
            f'Version updated from 0.0.0rc7 to 0.0.0b7\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--alpha', '7'], catch_exceptions=False).output),
            f'Version updated from 0.0.0b7 to 0.0.0a7\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--patch', '7'], catch_exceptions=False).output),
            f'Version updated from 0.0.0a7 to 0.0.7\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--minor', '7'], catch_exceptions=False).output),
            f'Version updated from 0.0.7 to 0.7.0\n')
        
        self.assertEqual(strip_color(runner.invoke(version, ['inc', '--major', '7'], catch_exceptions=False).output),
            f'Version updated from 0.7.0 to 7.0.0\n')
        
        self.assertRegex(strip_color(runner.invoke(version, ['inc', '--timestamp'], catch_exceptions=False).output),
            r'Version updated from 7.0.0 to 7.0.0\+\d{14}')
