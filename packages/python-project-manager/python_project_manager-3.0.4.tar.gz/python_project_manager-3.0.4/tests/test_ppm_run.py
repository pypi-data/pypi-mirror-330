import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_run import run
from python_project_manager.run_command import command_context
from tests.helper import working_directory

class TestPpmRun(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_run(self):
        captured_output = []
        with command_context(output_list=captured_output):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(run, ['start'], catch_exceptions=False)
            captured_output = '\n'.join(captured_output).strip()
            self.assertEqual(captured_output, 'Hello, World!, from test_project!')