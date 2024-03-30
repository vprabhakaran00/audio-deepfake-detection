from setuptools import setup, find_packages

__version__ = '0.0.0'

setup(
    name = 'audio-deepfake-detection',
    version = __version__,
    author = 'vprabhakaran00',
    author_email = 'vishnuprbhkrn@gmail.com',
    url = 'https://github.com/vprabhakaran00/audio-deepfake-detection',
    project_urls = {
        'Tracker': 'https://github.com/vprabhakaran00/audio-deepfake-detection/issues',
    },
    description = 'A classifier to detect whether an audio file is deepfaked or not.',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    package_dir = {'': 'src'},
    packages = find_packages(where = 'src')    
)
    
