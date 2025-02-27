from setuptools import setup, find_packages

setup(
    name="djangosetupheist",
    version="0.3",
    packages=find_packages(),
    install_requires=["django", "django-environ"],
    entry_points={
        "console_scripts": [
            "djs=djangosetupheist.cli:main",
        ],
    },
    author="eliHeist",
    description="A Django project setup automation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eliHeist/django_setup.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
