from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop  # Handle editable installs
import subprocess

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

class PostInstallCommand(install):
    """Post-installation command to run the script after install"""
    def run(self):
        install.run(self)  # Run the standard install process
        print("Running mindgraph/utils/dir.py after installation...")
        try:
            subprocess.run(["python", "-m", "mindgraph.utils.dir"], check=True)
            print("Successfully ran mindgraph/utils/dir.py")
        except Exception as e:
            print(f"Error running mindgraph/utils/dir.py: {e}")

class PostDevelopCommand(develop):
    """Post-installation command for editable installs"""
    def run(self):
        develop.run(self)  # Run the standard develop process
        print("Running mindgraph/utils/dir.py after editable install...")
        try:
            subprocess.run(["python", "-m", "mindgraph.utils.dir"], check=True)
            print("Successfully ran mindgraph/utils/dir.py")
        except Exception as e:
            print(f"Error running mindgraph/utils/dir.py: {e}")

setup(
    name='mindgraph',
    version='2025.3.1.0',
    author='Idin K',
    author_email='python@idin.net',
    description='A Python package for modeling knowledge as graphs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/idin/mindgraph',
    packages=find_packages(),
    license="Conditional Freedom License (CFL-1.0)",  # Keep this line
    install_requires=[
        'pandas>=2.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    scripts=["mindgraph/utils/dir.py"],  # Ensures the script is installed
    cmdclass={
        "install": PostInstallCommand,  # Runs script after standard install
        "develop": PostDevelopCommand,  # Runs script after editable install (-e)
    },
    python_requires='>=3.6',
    exclude_package_data={"": ["LICENSE"]},  # Force removal of LICENSE
)
