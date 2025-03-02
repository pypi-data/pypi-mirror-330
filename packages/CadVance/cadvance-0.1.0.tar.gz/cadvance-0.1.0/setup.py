# setup.py
from setuptools import setup, find_packages

setup(
    name="CadVance",  # Name of your package
    version="0.1.0",
    packages=find_packages(),  # Automatically finds the 'cadvance' package
    install_requires=[
        'pywin32',  # Required for COM interaction with AutoCAD
        'colorama',  # Required for colored logs
        'psutil',  # Required for process checking (is_autocad_running)
    ],
    entry_points={
        'console_scripts': [
            'cadvance = cadvance.__main__:main',  # Registers 'cadvance' as a command-line tool
        ],
    },
    keywords=["autocad", "automation", "activex", "comtypes"],
    author="Jones Peter",
    description="A professional AutoCAD automation package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    include_package_data=True,  # Include non-Python files, like the README
)
