import re
from setuptools import setup, find_packages
from pathlib import Path


HERE = Path(__file__).parent.resolve()

__INIT_PY__ = HERE.joinpath('src/stream_generator/__init__.py')


def find_version():
    with open(__INIT_PY__) as f:
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE
        )
        if version_match:
            return version_match.group(1)
        else:
            raise RuntimeError(f'Unable to find __version__ string in {__INIT_PY__}!')


setup(
    name='stream_generator',
    version=find_version(),
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires='>=3.7',
    entry_points="""
        [console_scripts]
        run_stream_generator=stream_generator.run_generator:main
    """
)
