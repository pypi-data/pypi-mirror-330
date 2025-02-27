from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent

VERSION = '0.0.2'
DESCRIPTION = """ Create asynchronous and asynchronous task
                    queues that run on a schedule... symantically """
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name="qmate",
    version=VERSION,
    author="Digital Kelvin",
    author_email="<qmate@digitalkelvin.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=[
        "events",
        "tasks",
        "queue",
        "schedules",
        "scheduling",
        "event loops"
    ]
)
