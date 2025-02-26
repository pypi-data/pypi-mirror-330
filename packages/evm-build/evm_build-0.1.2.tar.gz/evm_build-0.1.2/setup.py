from setuptools import setup, find_packages

setup(
    name="evm_build",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["requests"],  
    author="NekoBeko",
    author_email="nekobeko@gmail.com",
    description="A simple EVM validator for API requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
