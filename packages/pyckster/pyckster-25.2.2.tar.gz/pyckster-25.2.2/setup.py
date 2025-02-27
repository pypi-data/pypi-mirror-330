from setuptools import setup, find_packages

version = "25.2.2"

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pyckster",
    description="A PyQt5-based GUI for picking seismic traveltimes",
    author="Sylvain Pasquet",
    author_email="sylvain.pasquet@sorbonne-universite.fr",
    version=version,
    url='https://gitlab.in2p3.fr/metis-geophysics/pyckster',
    license='GPLv3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=[
        "PyQt5>=5.15.4",
        "pyqtgraph",
        "numpy",
        "scipy",
        "matplotlib",
        "obspy",
    ],
    py_modules=['pyckster'],
    entry_points={
        'console_scripts': [
            'pyckster=pyckster:main',
        ],
    },
    include_package_data=True,
    zip_safe=False
)