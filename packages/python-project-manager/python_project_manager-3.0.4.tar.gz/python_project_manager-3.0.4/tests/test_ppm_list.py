import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_list import list
from python_project_manager.run_command import command_context
from tests.helper import working_directory

# class TestPpmList(unittest.TestCase):
#     @working_directory(cwd='tests/__cached__')
#     def test_ppm_list(self):
#         captured_output = []
#         with command_context(output_list=captured_output):
#             Config.load()
#             runner = CliRunner()
#             runner.invoke(init, ['test_project'], catch_exceptions=False)
#             runner.invoke(list, catch_exceptions=False)
#             captured_output = '\n'.join(captured_output)
#             self.assertEqual(captured_output, '')

# class TestPpmList(unittest.TestCase):
#     @working_directory(cwd='tests/__cached__')
#     def test_ppm_list_help(self):
#         captured_output = []
#         with command_context(output_list=captured_output):
#             Config.load()
#             runner = CliRunner()
#             runner.invoke(init, ['test_project'], catch_exceptions=False)
#             runner.invoke(list, ['--help'], catch_exceptions=False)
#             captured_output = '\n'.join(captured_output)
#             self.assertEqual(captured_output, '')
    

