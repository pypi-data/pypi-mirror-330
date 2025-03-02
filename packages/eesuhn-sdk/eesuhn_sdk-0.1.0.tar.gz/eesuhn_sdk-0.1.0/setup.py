import pathlib

from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_desc = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='eesuhn-sdk',
    version='0.1.0',
    description='eesuhn\'s Personal SDK',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/eesuhn/eesuhn-sdk',
    author='eesuhn',
    author_email='eason.yihong@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='eesuhn',
    packages=find_packages(where='eesuhn-sdk'),
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'eesuhn=eesuhn:main',
        ],
    },
    project_urls={
        'Homepage': 'https://github.com/eesuhn/eesuhn-sdk',
        'Repository': 'https://github.com/eesuhn/eesuhn-sdk',
        'Issues': 'https://github.com/eesuhn/eesuhn-sdk/issues',
    }
)
