from setuptools import setup, find_packages

setup(
    name="django-ahin",  # Package name for installation (with hyphen)
    version="2.1.0",
    author="Ahindev .B",
    author_email="ahindev27@gmail.com",
    description="A tool to quickly generate Django projects with apps, templates, static files, models, and forms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AHINDEV/django-ahin",
    packages=find_packages(),  # This will find the `django_ahin` package
    install_requires=[
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "django-ahin=django_ahin.cli:main",  # Use the internal module name here
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)