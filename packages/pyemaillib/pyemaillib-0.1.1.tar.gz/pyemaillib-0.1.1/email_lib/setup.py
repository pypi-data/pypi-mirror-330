from setuptools import setup, find_packages

setup(
    name="pyemaillib",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Jinja2"
    ],
    author="Peniel Ben",
    description="A simple email sending library with Jinja2 templates",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
