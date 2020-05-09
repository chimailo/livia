from setuptools import setup

setup(
    name='Users_Livia',
    version='0.1',
    packages=['app.cli', 'app.cli.commands'],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        livia=app.cli.cli:cli
    ''',
)
