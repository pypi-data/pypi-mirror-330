from setuptools import setup, find_packages

setup(
    name="phpshift",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "phpshift=phpshift.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "phpshift": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/jobs.py",
            ".system/sources/clight.json",
            ".system/sources/logo.ico"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Pending",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "Operating System :: OS Independent",
    ],
)
