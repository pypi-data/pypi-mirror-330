from setuptools import setup, find_packages

setup(
    name="sklearnPra",  # Aapka package name
    version="1.4",  # Version update karein
    author="Your Name",
    author_email="your.email@example.com",
    description="A package that pastes predefined Python code into the current file",
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
