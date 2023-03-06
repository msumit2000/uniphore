from setuptools import setup, find_packages

setup(
    name="udops",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
    'console_scripts': [
            'udops= udops.__main__:app',
        ],
    },
)