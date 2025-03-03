from setuptools import setup, find_packages

setup(
    name="sklearnPra",
    version="0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sample package with extra Python files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/sklearnPra/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
