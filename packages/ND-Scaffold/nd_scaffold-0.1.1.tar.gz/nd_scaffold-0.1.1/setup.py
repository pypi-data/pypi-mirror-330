from setuptools import setup, find_packages

setup(
    name='ND-Scaffold',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'flask',
        'flask-restx',
        'sqlalchemy',
        'psycopg2-binary',
        'marshmallow',
        'alembic',
    ],
    entry_points={
        'console_scripts': [
            'nd-scaffold=scaffold.cli:cli',
        ],
    },
)
