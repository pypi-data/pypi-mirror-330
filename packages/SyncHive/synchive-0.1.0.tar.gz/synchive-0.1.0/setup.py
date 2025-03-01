from setuptools import setup, find_packages

setup(
    name="SyncHive",
    version="0.1.0",
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
)
