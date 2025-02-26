from setuptools import setup, find_packages

setup(
    name="django-ahin",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
    ],
    entry_points={
        "console_scripts": [
            "django-ahin=django_ahin.cli:main",
        ],
    },
    description="A CLI tool to generate a Django project with a predefined structure.",
    author="Ahindev",
    author_email="ahindev27@gmail.com",
    url="https://github.com/AHINDEV/django-ahin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)