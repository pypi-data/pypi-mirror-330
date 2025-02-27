from setuptools import setup, find_packages
setup(
    name="django-ahin",
    version="1.1.1",
    packages=find_packages(),  # Automatically find the `django_ahin` package
    install_requires=["Django>=4.0"],
    entry_points={
        "console_scripts": [
            "django-ahin=django_ahin.cli:main",  # Entry point for the CLI
        ],
    },
    description="A CLI tool to generate Django projects with apps, templates, and static files.",
    author="Ahindev",
    author_email="ahindev27@gmail.com.com",
    url="https://github.com/AHINDEV/django-ahin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)



