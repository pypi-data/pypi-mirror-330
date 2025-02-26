from setuptools import setup, find_packages

setup(
    name='django_ahin',
    version='1.16.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'django-ahin = django_ahin.create_project:main',
        ],
    },
)
