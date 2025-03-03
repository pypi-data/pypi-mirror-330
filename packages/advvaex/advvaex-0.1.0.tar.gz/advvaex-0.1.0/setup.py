from setuptools import setup, find_packages

setup(
    name="advvaex",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="your-email@example.com",
    description="An advanced extension of the Vaex library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/advvaex",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "vaex>=4.0.0",
    ],
)