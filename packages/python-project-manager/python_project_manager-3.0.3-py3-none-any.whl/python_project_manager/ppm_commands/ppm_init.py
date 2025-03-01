import os
import click
from python_project_manager.config import Config
from python_project_manager.run_command import run_command

class Initializer:
    def __init__(self) -> None:
        '''
        Tracks the configuration values, files and folders to be created for the project
        Args:
            project_name (str): The name of the project
            config_file_name (str): The name of the configuration file to be created in the project folder
        '''
        self.config_values = {}
        self.files = {}
        self.folder = []

        self.AddConfigValue('project_name', '')
        self.AddConfigValue('version', '0.0.0b1')
        self.AddConfigValue('src_dir', '')
        self.AddConfigValue('include_paths', [])
        self.AddConfigValue('pip.extra_index_url', [])
        self.AddConfigValue('pip.trusted_host', [])
        self.AddConfigValue('scripts', {})
        self.AddFile('requirements.txt', None)
        self.AddFile('requirements-dev.txt', None)

    def AddConfigValue(self, key: str, value: str) -> None:
        '''
        Adds a configuration value to the project

        Args:
            key (str): The key of the configuration value.
                Key is a dot-separated string that represents the path to the configuration value.
                For example: 'scripts.start' is equivalent to ['scripts']['start'].
            value (any): The value of the configuration value.
        '''
        self.config_values[key] = value
        
    def AddFile(self, path: str, content: str) -> None:
        '''
        Adds a file to the project

        Args:
            path (str): The path of the file to be created.
                Converted to an absolute path before being added.
            content (str): The content of the file.
                None = Empty file.
        '''
        self.files[os.path.abspath(path)] = content

    def AddFolder(self, path: str) -> None:
        '''
        Adds a folder to the project

        Args:
            path (str): The path of the folder to be created.
                Converted to an absolute path before being added.
        '''
        self.folder.append(os.path.abspath(path))

    def Initialize(self) -> None:
        '''
        Saves the configuration values to the project and creates the files and folders.
        '''
        # Add the configuration values to the project
        from python_project_manager.config import Config
 
        for key, value in self.config_values.items():
            Config.set(key, value)
        Config.save()

        # Create all the folder paths
        for folder in self.folder:
            os.makedirs(folder, exist_ok=True)

        # Create all the files, if the path does not exist create the folder first, if content is None, create an empty file
        for path, content in self.files.items():
            folder = os.path.dirname(path)
            os.makedirs(folder, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content or '')


@click.command()
@click.argument('project_name', type=str, required=True)
@click.option('--force', '-f', is_flag=True, help='Force the initialization project, even if the directory is not empty')
def init(project_name: str, force: bool) -> None:
    '''
    <project_name>: The name of the project
    '''
    src_path = 'src'

    # Check if the project has already been initialized
    if not force and len(os.listdir(os.getcwd())) != 0:
        print('Project already initialized')
        return
    
    initializer = Initializer()
    initializer.AddConfigValue('project_name', project_name)
    initializer.AddConfigValue('src_dir', src_path)
    initializer.AddConfigValue('paths', [src_path])
    initializer.AddConfigValue('scripts.start', 'py -m %src_dir%.main')
    initializer.AddFile(f'{src_path}/main.py',
        f'''if __name__ == '__main__':
    print('Hello, World!, from {project_name}!')''')

    initializer.Initialize()
    run_command('python -m venv venv', use_venv=False)
    print(f'Project {project_name} created')