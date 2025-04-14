from setuptools import setup, find_packages

setup(
    name="dev_tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    entry_points={
        'console_scripts': [
            'dev_tool=dev_tool.cli:main',
        ],
    },
)