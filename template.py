import os
from pathlib import Path
import logging

logging.basicConfig(format = '%(asctime)s : %(message)s', level = logging.INFO)

project_name = 'audioClassifier'

list_of_files = [
    ".github/workflows/.gitkeep",
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/config/config.py',
    f'src/{project_name}/pipeline/__init__.py',
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/constants/__init__.py',
    'templates/index.html',
    'config/config.yaml',
    'dvc.yaml',
    'params.yaml',
    'requirements.txt',
    'setup.py',
    'research/trials.ipynb'
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, _ = os.path.split(filepath)
    
    # Creating the directories
    if filedir != '':
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Creating directory - {filedir}')
    
    # Creating the files    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f'Creating empty file - {filepath}')     
    else:
        logging.info(f'{filename} already exists')