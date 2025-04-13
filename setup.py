from setuptools import setup, find_packages

setup(
    name="dtl",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    entry_points={
        'console_scripts': [
            'dtl=auto_commit.cli:main',
        ],
    },
)