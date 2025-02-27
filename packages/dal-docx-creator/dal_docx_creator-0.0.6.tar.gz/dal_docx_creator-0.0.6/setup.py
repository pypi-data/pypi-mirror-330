from setuptools import setup, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'DOCX Creator'
LONG_DESCRIPTION = 'Library to play with DOCXs and generate them'

setup(
    name = "dal_docx_creator", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'python-docx',
        'comtypes',
        'yta_general_utils',
    ],
    
    keywords = [
        'docx creator',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)