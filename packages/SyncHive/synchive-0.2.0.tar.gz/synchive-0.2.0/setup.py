from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="SyncHive",
    version="0.2.0",
    author="Harsh Mistry",
    author_email="hmistry864@gmail.com",
    description="Automated file backup and synchronization over SSH within a shared network for seamless data management.",
    packages=find_packages(),
    install_requires=["paramiko", "watchdog", "setuptools", "wheel", "twine"],
    entry_points={
        "console_scripts": [
            "synchive = synchive.cli:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)
