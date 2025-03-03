from setuptools import setup, find_packages

setup(
    name="pyshell-bash",
    version="0.1.0a2",
    description="An interactive bash/sh shell in Python",
    author="SteveGaming62",
    author_email="anon@dev.com",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'pyshell=pyshell:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
